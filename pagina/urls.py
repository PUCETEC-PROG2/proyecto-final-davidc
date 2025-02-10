from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('set-theme/<str:theme>/', views.set_theme, name='set_theme'),
    path('clientes/', views.clientes, name='clientes'),
    path('compras/', views.compras, name='compras'),
    path('catalogo/', views.catalogo, name='catalogo'),
]   