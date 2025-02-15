from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from decimal import Decimal  # Agregar esta importación
from .states import EstadoDisponible, EstadoVendido
from .utils.pdf_generator import generar_contrato  # Agregar esta importación



def validar_cedula_ecuatoriana(cedula):
    """
    Valida la cédula ecuatoriana según el algoritmo oficial.
    """
    if not cedula.isdigit() or len(cedula) != 10:
        raise ValidationError("La cédula debe tener 10 dígitos numéricos.")

    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    digitos = list(map(int, cedula))
    suma = sum((digito * coef if digito * coef < 10 else digito * coef - 9) for digito, coef in zip(digitos[:9], coeficientes))
    digito_verificador = (10 - (suma % 10)) % 10

    if digito_verificador != digitos[9]:
        raise ValidationError("La cédula ecuatoriana no es válida.")


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Propiedad(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='propiedades')
    ubicacion = models.CharField(max_length=255)
    metros_cuadrados = models.PositiveIntegerField()
    habitaciones = models.PositiveIntegerField()
    banos = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=[('disponible', 'Disponible'), ('vendido', 'Vendido')], default='disponible')
    imagen = models.ImageField(upload_to='propiedades/', null=True, blank=True)
    numero_particular = models.CharField(max_length=50, blank=True, null=True)  # Agrega este campo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)[:100]
        super().save(*args, **kwargs)


    @property
    def estado_actual(self):
        if self.estado == 'disponible':
            return EstadoDisponible()
        return EstadoVendido()

    def vender(self):
        if self.esta_disponible():
            self.estado = 'vendido'
            self.save()
            return True
        return False

    def esta_disponible(self):
        return self.estado == 'disponible'

    def get_estado_display(self):
        return dict(self._meta.get_field('estado').choices)[self.estado]

    def __str__(self):
        return f"{self.nombre} - {self.categoria.nombre}"
    
class PropiedadImagen(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='propiedad_imagenes/')

    def __str__(self):
        return f"Imagen de {self.propiedad.nombre}"
    
class Cliente(models.Model):
    primer_nombre = models.CharField(max_length=20)
    segundo_nombre = models.CharField(max_length=20, blank=True, null=True)
    primer_apellido = models.CharField(max_length=20)
    segundo_apellido = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, validators=[EmailValidator(message="Ingrese un correo válido.")])
    cedula = models.CharField(
        max_length=10,
        unique=True,
        validators=[validar_cedula_ecuatoriana]
    )
    
    telefono = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex='^\d{10}$', message="El teléfono debe tener 10 dígitos.")]
    )
    telefono_fijo = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        validators=[RegexValidator(regex='^\d{7}$', message="El teléfono fijo debe tener 7 dígitos.")]
    )
    direccion = models.TextField(blank=False, null=False)    # Campo dirección

    def __str__(self):
        return f"{self.primer_nombre} {self.segundo_nombre or ''} {self.primer_apellido} {self.segundo_apellido or ''}".strip()

class Compra(models.Model):
    propiedades = models.ManyToManyField(Propiedad, related_name='compras')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='compras')
    fecha_compra = models.DateTimeField()
    precio_sin_iva = models.DecimalField(max_digits=10, decimal_places=2)
    precio_con_iva = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    contrato = models.FileField(upload_to='contratos/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        if self.precio_sin_iva:
            self.precio_con_iva = self.precio_sin_iva * Decimal('1.15')
        
        # Primer guardado para obtener el ID
        super().save(*args, **kwargs)
        
        if is_new:  # Solo si es una nueva compra
            # Forzar la recarga de las relaciones many-to-many
            self.refresh_from_db()
            
            # Generar el contrato después de que todas las relaciones estén guardadas
            try:
                filename = generar_contrato(self)
                self.contrato.name = f'contratos/{filename}'
                super().save(update_fields=['contrato'])
            except Exception as e:
                print(f"Error al generar el contrato: {e}")
            
            # Cambiar estado de las propiedades
            for propiedad in self.propiedades.all():
                if propiedad.esta_disponible():
                    propiedad.vender() 
                    
    def __str__(self):
        return f"Compra de {', '.join(p.nombre for p in self.propiedades.all())} por {self.cliente.primer_nombre} {self.cliente.primer_apellido}- ${self.precio_con_iva} (con IVA)"
