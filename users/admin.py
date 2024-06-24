from django.contrib import admin
from .models import Asesor, Sucursale, File, CooviahorroMonth, Court, Subzona, CrecimientoCdatMonth,CountCrecimientoCDAT

@admin.register(Asesor)
class AsesorAdmin(admin.ModelAdmin):
    list_display = ['name', 'rol', 'sucursal', 'subzona']
    
@admin.register(Sucursale)
class SucursalesAdmin(admin.ModelAdmin):
    list_display = ['city']
    
@admin.register(Subzona)
class SubzonaAdmin(admin.ModelAdmin):
    list_display = ['subzona']
    
@admin.register(File)
class FilesAdmin(admin.ModelAdmin):
    list_display = ['month', 'year', 'full_date', 'created']

@admin.register(CooviahorroMonth)
class CooviahorroMonthAdmin(admin.ModelAdmin):
    list_display = ['nameAsesor', 'totalValue', 'year', 'month', 'court']

@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ['value']

@admin.register(CountCrecimientoCDAT)
class CountCrecimientoCDATAdmin(admin.ModelAdmin):
    list_display = ['value']

@admin.register(CrecimientoCdatMonth)
class CrecimientoCdatMonthAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'year', 'month']