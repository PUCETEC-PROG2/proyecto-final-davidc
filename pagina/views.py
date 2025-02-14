from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Propiedad
from .models import Cliente
from django.db.models import Q
from .models import Compra
from .models import Cliente
from .forms.ClienteForm import ClienteForm
from .forms.CompraForm import CompraForm
from django.db.models import Sum
from .models import Compra
from .generar_contrato_pdf import generar_contrato_pdf # Importa la función para generar el contrato PDF
from django.core.files import File  # Importa File para guardar el contrato en el sistema de archivos
from decimal import Decimal  # Importa Decimal

def home(request):
    propiedades_recientes = Propiedad.objects.all().order_by("-id")[:5]
    # Opcional: para depurar, puedes imprimir el conteo
    print("Propiedades recientes:", propiedades_recientes.count())
    return render(request, "home.html", {"propiedades_recientes": propiedades_recientes})

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def clientes(request):
    return render(request, 'clientes.html')

def clientes_list(request):
    clientes = Cliente.objects.all()
    return render(request, "clientes.html", {"clientes": clientes})

def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes_list')
    else:
        form = ClienteForm()
    return render(request, 'cliente_form.html', {'form': form})

def cliente_edit(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente_form.html', {'form': form})

def cliente_delete(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes_list')
    return render(request, 'cliente_confirm_delete.html', {'cliente': cliente})

@login_required
@user_passes_test(is_staff)
def compras(request):
    return render(request, 'compras.html')

@login_required
@user_passes_test(is_staff)
def catalogo(request):
    return render(request, 'catalogo.html')

def set_theme(request, theme):
    request.session['theme'] = theme
    return render(request, 'home.html', {'theme': theme})

def departamentos(request):
    # Suponiendo que en el modelo Propiedad existe un campo o relación que indique la categoría.
    # Por ejemplo, si tienes un ForeignKey a "Categoria" y el nombre de la categoría es "Departamento":
    departamentos = Propiedad.objects.filter(categoria__nombre__iexact='departamentos')
    return render(request, 'departamentos.html', {'departamentos': departamentos})

def display_departamento(request, slug):
    departamento = get_object_or_404(Propiedad, slug=slug)
    return render(request, 'display_departamento.html', {'propiedad': departamento})

def casas(request):
    casas = Propiedad.objects.filter(categoria__nombre__iexact='casas')
    return render(request, 'casas.html', {'casas': casas}) 

def buscar_propiedades(request):
    query = request.GET.get('q', '')
    if query:
        resultados = Propiedad.objects.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(ubicacion__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )
    else:
        resultados = []
    context = {'resultados': resultados, 'query': query}
    return render(request, 'buscar_propiedades.html', context) 

def compras(request):
    compras = Compra.objects.all()
    return render(request, 'compras.html', {'compras': compras})

def compra_detail(request, compra_id):
    compra = get_object_or_404(Compra, pk=compra_id)
    return render(request, 'compra_detail.html', {'compra': compra}) 


def compra_create(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            
            # Save the compra first
            propiedades_seleccionadas = form.cleaned_data['propiedades']
            
            # Calculate prices
            compra.precio_sin_iva = propiedades_seleccionadas.aggregate(Sum('precio'))['precio__sum'] or 0
            compra.precio_con_iva = compra.precio_sin_iva * Decimal('1.15')  # Convierte 1.15 a Decimal
            
            compra.save()
            form.save_m2m()  # This saves the many-to-many relationships
            # Generate PDF with selected properties
            # try:
            #     generar_contrato_pdf(compra, propiedades_seleccionadas)
                
            #     # Save the contract
            #     with open(f"contrato_{compra.id}.pdf", 'rb') as f:
            #         compra.contrato.save(f"contrato_{compra.id}.pdf", File(f), save=True)
            # except Exception as e:
            #     print(f"Error generating or saving contract: {e}")

            return redirect('compras')
    else:
        form = CompraForm()
    return render(request, 'compra_form.html', {'form': form, 'title': 'Crear Compra'})