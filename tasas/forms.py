from .models import Afiliaciones
from django import forms

class AfiliacionesForm(forms.ModelForm):
    """"""
    class Meta():
        model = Afiliaciones
        fields = ['name', 'description', 'rol', 'since', 'until', 'value']
        labels = {
            'name': 'Nombre',
            'description': 'Descripcion',
            'rol': 'Rol',
            'since': 'Desde',
            'until': 'Hasta',
            'value': 'Valor'
        }