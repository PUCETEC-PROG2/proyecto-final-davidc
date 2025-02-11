from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Propiedad

def home(request):
    propiedades_recientes = Propiedad.objects.all().order_by("-id")[:5]
    # Opcional: para depurar, puedes imprimir el conteo
    print("Propiedades recientes:", propiedades_recientes.count())
    return render(request, "home.html", {"propiedades_recientes": propiedades_recientes})


    return render(request, 'home.html') 

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def clientes(request):
    return render(request, 'clientes.html')

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