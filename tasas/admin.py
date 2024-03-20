from django.contrib import admin
from .models import Afiliaciones, Colocaciones

@admin.register(Afiliaciones)
class AfiliacionesAdmin(admin.ModelAdmin):
    list_display = ['name', 'rol', 'since', 'until', 'value']
    
@admin.register(Colocaciones)
class ColocacionesAdmin(admin.ModelAdmin):
    list_display = ['name', 'rol', 'value_min', 'value_max', 'value']
