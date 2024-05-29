from django.db import models
from django.contrib.postgres.fields import ArrayField
from roles.models import Roles

class Afiliaciones(models.Model):
    """"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    rol = models.CharField(max_length=200)
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
        return f"Cdats {self.type} desde {self.valueMin} hasta {self.valueMax}"

class CdatTasas(models.Model):
    """"""
    plazoMin = models.CharField(max_length=100)
    plazoMax = models.CharField(max_length=100)
    valueMin = models.CharField(max_length=100)
    valueMax = models.CharField(max_length=100)
    tasa = models.FloatField()
    
    def __str__(self):
        return f"Tasa {self.tasa}: Dias {self.plazoMin} - {self.plazoMax}, Monto: {self.valueMin} - {self.valueMax}"