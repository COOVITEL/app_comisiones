from django.contrib import admin
from .models import Asesor, Sucursales

@admin.register(Asesor)
class AsesorAdmin(admin.ModelAdmin):
    list_display = ['name', 'sucursal']
    
@admin.register(Sucursales)
class SucursalesAdmin(admin.ModelAdmin):
    list_display = ['city']