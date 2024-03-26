from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import File, Asesor

class FileForm(ModelForm):
    """"""
    class Meta:
        model = File
        fields = ['month', 'year', 'file']
        labels = {
            'month': 'Mes',
            'year': 'Año',
            'file': 'Archivo'
        }
        
    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data.get('year')
        month = cleaned_data.get('month')
        
        file = cleaned_data.get('file')
        
        
        if ".xlsx" in file:
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