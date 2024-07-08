from .models import *
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
        labels= {
            'plazoMin': 'Plazo minimo en dias',
            'plazoMax': 'Plazo maximo en dias',
            'valueMin': 'Valor minimo',
            'valueMax': 'Valor maximo',
            'tasa': 'Tasa'
        }            

class AhorroVistaForm(forms.ModelForm):
    """"""
    valueMin = forms.CharField(widget=forms.TextInput(attrs={'oninput': "handleChange('id_valueMin')"}),
                               label="Valor minimo")
    valueMax = forms.CharField(widget=forms.TextInput(attrs={'oninput': "handleChange('id_valueMax')"}),
                               label="Valor maximo")

    class Meta():
        model = AhorroVista
        fields = ['valueMin', 'valueMax', 'porcentaje']
        labels = {
            'porcentaje': 'Porcentaje'
        }

class CrecimientoBaseSocialForm(forms.ModelForm):
    """"""
    value = forms.CharField(widget=forms.TextInput(attrs={'oninput': "handleChange('id_value')"}),
                            label="Valor por afiliación")
    
    class Meta():
        model = CrecimientoBaseSocial
        fields = ['porcentaje', 'value']
        labels = {
            'porcentaje': 'Porcentaje Minimo para aplicar',
        }

class CrecimientoCDATForm(forms.ModelForm):
    """"""
    medida = forms.CharField(widget=forms.TextInput(attrs={'oninput': "handleChange('id_medida')"}),
                             label="Valor de medida de comisión")
    comision = forms.CharField(widget=forms.TextInput(attrs={'oninput': "handleChange('id_comision')"}),
                               label="Valor de comision")
    class Meta:
        model = CrecimientoCDAT
        fields = ['medida', 'tasaMin', 'tasaMax', 'comision']
        labels = {
            'tasaMin': 'Tasa minima promedio',
            'tasaMax': 'Tasa maxima promedio',
        }

class CrecimientoCooviahorroForm(forms.ModelForm):
    """"""
    value = forms.CharField(widget=forms.TextInput(attrs={'oninput': "handleChange('id_value')"}),
                            label="Valor a pagar por millon $1.000.000")
    class Meta:
        model = CrecimientoCooviahorro
        fields = ['description', 'value']
        labels = {
            'description': 'Descripcion',
            }

class CrecimientoAhorroVistaForm(forms.ModelForm):
    """"""
    valueMin = forms.CharField(widget=forms.TextInput(attrs={'oninput': "handleChange('id_valueMin')"}),
                            label="Saldo promedio minimo")
    valueMax = forms.CharField(widget=forms.TextInput(attrs={'oninput': "handleChange('id_valueMax')"}),
                            label="Saldo promedio maximo")
    
    class Meta:
        model = CrecimientoAhorroVista
        fields = ['description', 'valueMin', 'valueMax', 'porcentaje']
        labels = {
            'description': 'Descripcion',
            'procentaje': 'Porcentaje sobre el saldo promedio'
        }

class CrecimientoCarteraForm(forms.ModelForm):
    """"""
    valueMin = forms.CharField(widget=forms.TextInput(attrs={'oninput': "handleChange('id_valueMin')"}),
                            label="Valor minimo de Crecimiento")
    valueMax = forms.CharField(widget=forms.TextInput(attrs={'oninput': "handleChange('id_valueMax')"}),
                            label="Valor maximo de Crecimiento")
    value = forms.CharField(widget=forms.TextInput(attrs={'oninput': "handleChange('id_value')"}),
                            label="Valor de comision por millon ($1.000.000)")

    class Meta:
        model = CrecimientoCartera
        fields = ["description", "tasaMin", "tasaMax", "valueMin", "valueMax", "value"]
        labels = {
            "description": "Descripcion",
            "tasaMin": "Tasa minima promedio CDATs",
            "tasaMax": "Tasa Maxima promedio CDATs",
            "value": "Valor comision"
        }