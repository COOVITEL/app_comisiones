from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Sucursale, Subzona, File, Asesor

class SucursalForm(ModelForm):
    class Meta:
        model = Sucursale
        fields = ['city']
        labels = {'city': 'Ciudad'}

class SubzonaForm(ModelForm):
    class Meta:
        model = Subzona
        fields = ['subzona']
        labels = {'subzona': 'Subzona'}

class FileForm(ModelForm):
    """"""
    class Meta:
        model = File
        fields = ['month', 'year', 'fileComisiones', 'fileAhorroVista', 'fileCrecimientoBase', 'fileCrecimientoCDAT']
        labels = {
            'month': 'Mes',
            'year': 'Año',
            'fileComisiones': 'Archivo Comisiones',
            'fileAhorroVista': 'Archivo Ahorro Vista',
            'fileCrecimientoBase': 'Archivo Crecimiento Base',
            'fileCrecimientoCDAT': 'Archivo Crecimiento CDAT'
        }
        
    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data.get('year')
        month = cleaned_data.get('month')
        
        fileComisiones = cleaned_data.get('fileComisiones')
        fileAhorroVista = cleaned_data.get('fileAhorroVista')
        fileCrecimientoBase = cleaned_data.get('fileCrecimientoBase')
        fileCrecimientoCDAT = cleaned_data.get('fileCrecimientoCDAT')
        
        if all(".xlsx" in archivo for archivo in (fileComisiones, fileAhorroVista, fileCrecimientoBase, fileCrecimientoCDAT)):
            raise ValidationError("El archivo debe ser de formato xlsx")
        
        if File.objects.filter(year=year, month=month).exists():
            raise ValidationError(f"Ya existe un registro para ese mes y año.")
        return cleaned_data

class AsesorForm(ModelForm):
    class Meta:
        model = Asesor
        fields = ['name', 'rol', 'sucursal', 'subzona']
        labels = {
            'name': 'Nombre',
            'rol': 'Rol del asesor',
            'sucursal': 'Sucursal',
            'subzona': 'Subzona'
        }