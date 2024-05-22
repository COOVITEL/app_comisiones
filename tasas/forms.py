from .models import Afiliaciones, Colocaciones
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

class ColocacionesForm(forms.ModelForm):
    """"""
    class Meta():
        model = Colocaciones
        fields = [
            'name',
            'description',
            'rol',
            'tasa_min',
            'tasa_max',
            'value_min',
            'value_max',
            'value'
        ]
        labels = {
            'name': 'Nombre',
            'description': 'Descripcion',
            'rol': 'Rol',
            'tasa_min': 'Tasa Minima',
            'tasa_max': 'Tasa Maxima',
            'value_min': 'Valor Minimo',
            'value_max': 'Valor Maximo',
            'value': 'Valor Comision'
        }