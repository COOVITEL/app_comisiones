from django.contrib import admin
from .models import Asesor, Sucursale, File

@admin.register(Asesor)
class AsesorAdmin(admin.ModelAdmin):
    list_display = ['name', 'sucursal']
    
@admin.register(Sucursale)
class SucursalesAdmin(admin.ModelAdmin):
    list_display = ['city']
    
@admin.register(File)
class FilesAdmin(admin.ModelAdmin):
    list_display = ['month', 'year', 'full_date']