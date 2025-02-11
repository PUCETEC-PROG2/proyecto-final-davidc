from django.contrib import admin
from .models import Propiedad, Cliente, Compra, Categoria

# Register your models here.
admin.site.register(Propiedad)
admin.site.register(Cliente)
admin.site.register(Compra)
admin.site.register(Categoria)
