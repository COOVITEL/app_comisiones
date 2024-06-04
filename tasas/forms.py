from .models import Afiliaciones, Colocaciones, Cooviahorro, Cdat, CdatTasas, AhorroVista
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

class CooviahorroForm(forms.ModelForm):
    """"""
    class Meta():
        model = Cooviahorro
        fields = ['name', 'description', 'rol', 'monto', 'value']
        labels = {
            'name': 'Nombre',
            'description': 'Descripcion',
            'rol': 'Rol',
            'monto': 'Monto para comision',
            'value': 'Monto de comision'
        }

class CdatForm(forms.ModelForm):
    """"""
    class Meta():
        model = Cdat
        fields = ['name', 'description', 'rol', 'type', 'valueMin', 'valueMax', 'value']
        labels = {
            'name': 'Nombre',
            'description': 'Descriptión',
            'rol': 'Rol',
            'type': 'Tipo de Cdat',
            'valueMin': 'Valor Minimo',
            'valueMax': 'Valor Maximo',
            'value': 'Valor Comisión'
        }
        
class CdatTasasForm(forms.ModelForm):
    """"""
    class Meta():
        model = CdatTasas
        fields = ['plazoMin', 'plazoMax', 'valueMin', 'valueMax', 'tasa']
        labels= [
            {'plazoMin': 'Plazo minimo en dias'},
            {'plazoMax': 'Plazo maximo en dias'},
            {'valueMin': 'Valor minimo'},
            {'valueMin': 'Plazo minimo'},
            {'tasa': 'Tasa'}
            
        ]

class AhorroVistaForm(forms.ModelForm):
    """"""
    valueMin = forms.CharField(widget=forms.TextInput(attrs={'oninput': "handleChange('id_valueMin')"}))
    valueMax = forms.CharField(widget=forms.TextInput(attrs={'oninput': "handleChange('id_valueMax')"}))

    class Meta():
        model = AhorroVista
        fields = ['valueMin', 'valueMax', 'porcentaje']
        labels = [
            {'valueMin': 'Valor minimo'},
            {'valueMax': 'Valor maximo'},
            {'porcentaje': 'Porcentaje'}
        ]