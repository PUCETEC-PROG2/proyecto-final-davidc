from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils.text import slugify
from django.core.exceptions import ValidationError



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
    slug = models.SlugField(unique=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='propiedades')
    ubicacion = models.CharField(max_length=255)
    metros_cuadrados = models.PositiveIntegerField()
    habitaciones = models.PositiveIntegerField()
    banos = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=[('disponible', 'Disponible'), ('vendido', 'Vendido')], default='disponible')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.nombre} - {self.categoria.nombre}"
    
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
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='compras')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='compras')
    fecha_compra = models.DateTimeField(auto_now_add=True)
    precio_sin_iva = models.DecimalField(max_digits=10, decimal_places=2)
    precio_con_iva = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Precio con IVA

    def save(self, *args, **kwargs):
        if not self.precio_sin_iva:
            self.precio_sin_iva = self.propiedad.precio  # Toma el precio automáticamente
        self.precio_con_iva = round(self.precio_sin_iva * 1.15, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compra de {self.propiedad.nombre} por {self.cliente.primer_nombre} {self.cliente.primer_apellido}- ${self.precio_con_iva} (con IVA)"
