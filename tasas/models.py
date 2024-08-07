from django.db import models
from django.contrib.postgres.fields import ArrayField
from roles.models import Roles

class Afiliaciones(models.Model):
    """"""
    name = models.CharField(max_length=100)
    since = models.IntegerField()
    until = models.IntegerField()
    value = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return f"{self.name}: Desde {self.since} hasta {self.until}"

class Colocaciones(models.Model):
    """"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    rol = models.CharField(max_length=200)
    tasa_min = models.CharField(max_length=20)
    tasa_max = models.CharField(max_length=20)
    value_min = models.CharField(max_length=100)
    value_max = models.CharField(max_length=100, null=True)
    value = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return f"Colocaciones {self.name} de {self.rol}"

class Cooviahorro(models.Model):
    """"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    monto = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        """"""
        return f"Coviahoorro comision {self.value} por cada $ {self.monto} para {self.rol}"
    
class Cdat(models.Model):
    """"""
    CDATTYPE= [
        ('nuevo', 'Nuevo'),
        ('renovado', 'Renovado'),
    ]

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=CDATTYPE)
    valueMin = models.CharField(max_length=100)
    valueMax = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Cdats {self.rol} {self.type} desde {self.valueMin} hasta {self.valueMax}, comision: {self.value}"

class CdatTasas(models.Model):
    """"""
    plazoMin = models.CharField(max_length=100)
    plazoMax = models.CharField(max_length=100)
    valueMin = models.CharField(max_length=100)
    valueMax = models.CharField(max_length=100)
    tasa = models.FloatField()
    
    def __str__(self):
        return f"Tasa {self.tasa}: Dias {self.plazoMin} - {self.plazoMax}, Monto: {self.valueMin} - {self.valueMax}"

class AhorroVista(models.Model):
    """"""
    valueMin = models.CharField(max_length=100)
    valueMax = models.CharField(max_length=100)
    porcentaje = models.FloatField()
    
    def __str__(self):
        return f"Pago por ahorro vista por promedio mayor a {self.valueMin} y menor a {self.valueMax}, paga el {self.porcentaje}"

class CrecimientoBaseSocial(models.Model):
    """"""
    porcentaje = models.FloatField()
    value = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Etsa comision aplica si se supera el {self.porcentaje}, un valor de {self.value} por afiliacion"

class CrecimientoCDAT(models.Model):
    """"""
    medida = models.CharField(max_length=100)
    tasaMin = models.FloatField()
    tasaMax = models.FloatField()
    comision = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Comision Crecimiento CDAT: {self.comision} entre tasas del {self.tasaMin} - {self.tasaMax}"

class CrecimientoCooviahorro(models.Model):
    """"""
    description = models.CharField(max_length=500)
    value = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Comision $ {self.value} pagada por $ 1.000.000 de crecimiento en Cooviahorro a los directores de canal o sucursal"

class CrecimientoAhorroVista(models.Model):
    """"""
    description = models.CharField(max_length=500)
    valueMin = models.CharField(max_length=500)
    valueMax = models.CharField(max_length=500)
    porcentaje = models.FloatField()
    
    def __str__(self):
        return f"Comision creciemiento Ahorro Vista del {self.porcentaje} por montos desde {self.valueMin} hasta {self.valueMax}"

class CrecimientoCartera(models.Model):
    """"""
    description = models.CharField(max_length=500)
    tasaMin = models.FloatField()
    tasaMax = models.FloatField()
    valueMin = models.CharField(max_length=100)
    valueMax = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Comision por millon de {self.value} por tasas promedio entre {self.tasaMin} - {self.tasaMax}"
    