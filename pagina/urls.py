from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('set-theme/<str:theme>/', views.set_theme, name='set_theme'),
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/create/', views.cliente_create, name='cliente_create'),
    path('clientes/edit/<int:cliente_id>/', views.cliente_edit, name='cliente_edit'),
    path('clientes/delete/<int:cliente_id>/', views.cliente_delete, name='cliente_delete'),
    path('compras/', views.compras, name='compras'),
    path('compras/crear/', views.crear_compra, name='crear_compra'),
    path('compra/<int:compra_id>/', views.compra_detail, name='compras_detail'),
    path('departamentos/', views.departamentos, name='departamentos'),
    path('departamentos/<slug:slug>/', views.display_departamento, name='display_departamento'),
    path('casas/', views.casas, name='casas'),
    path('casas/<slug:slug>', views.display_casa, name='display_casa'),
    path('buscar/', views.buscar_propiedades, name='buscar_propiedades'),
    path('contactos/', views.contactos, name='contactos'),

]   