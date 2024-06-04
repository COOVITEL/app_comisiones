from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import File, Asesor

class FileForm(ModelForm):
    """"""
    class Meta:
        model = File
        fields = ['month', 'year', 'fileComisiones', 'fileAhorroVista']
        labels = {
            'month': 'Mes',
            'year': 'Año',
            'fileComisiones': 'Archivo Comisiones',
            'fileAhorroVista': 'Archivo Ahorro Vista'
        }
        
    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data.get('year')
        month = cleaned_data.get('month')
        
        fileComisiones = cleaned_data.get('fileComisiones')
        fileAhorroVista = cleaned_data.get('fileAhorroVista')
        
        if ".xlsx" in fileComisiones and ".xlsx" in fileAhorroVista:
            raise ValidationError("El archivo debe ser de formato xlsx")
        
        if File.objects.filter(year=year, month=month).exists():
            raise ValidationError(f"Ya existe un archivo para ese mes y año.")
        return cleaned_data

class AsesorForm(ModelForm):
    class Meta:
        model = Asesor
        fields = ['name', 'rol', 'sucursal']
        labels = {
            'name': 'Nombre',
            'rol': 'Rol del asesor',
            'sucursal': 'Sucursal'
        }