from django.contrib import admin
from .models import *

@admin.register(Afiliaciones)
class AfiliacionesAdmin(admin.ModelAdmin):
    list_display = ['name', 'rol', 'since', 'until', 'value']
    
@admin.register(Colocaciones)
class ColocacionesAdmin(admin.ModelAdmin):
    list_display = ['name', 'rol', 'value_min', 'value_max', 'value']

@admin.register(Cooviahorro)
class CooviahorroAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'rol', 'monto', 'value']

@admin.register(Cdat)
class CdatAdmin(admin.ModelAdmin):
    list_display = ['name', 'rol', 'type', 'valueMin', 'valueMax', 'value']

@admin.register(CdatTasas)
class CdatTasasAdmin(admin.ModelAdmin):
    list_display = ['plazoMin', 'plazoMax', 'valueMin', 'valueMax', 'tasa']
    
@admin.register(AhorroVista)
class AhorroVistaAdmin(admin.ModelAdmin):
    list_display = ['valueMin', 'valueMax', 'porcentaje']

@admin.register(CrecimientoBaseSocial)
class CrecimientoBaseSocialAdmin(admin.ModelAdmin):
    list_display = ['porcentaje', 'value']
    
@admin.register(CrecimientoCDAT)
class CrecimientoCDATAdmin(admin.ModelAdmin):
    list_display = ['medida', 'tasaMin', 'tasaMax', 'comision']

@admin.register(CrecimientoCooviahorro)
class CrecimientoCooviahorroAdmin(admin.ModelAdmin):
    list_display = ['description', 'value']