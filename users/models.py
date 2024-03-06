from django.db import models

class Sucursales(models.Model):
    """"""
    city = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.city

class Asesor(models.Model):
    """"""
    name = models.CharField(max_length=100)
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name