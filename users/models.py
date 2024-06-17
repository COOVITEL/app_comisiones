from django.db import models
from roles.models import Roles
import calendar

MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]
YEAR_CHOICES = [(i, i) for i in range(2023, 2040)]

class Sucursale(models.Model):
    """"""
    city = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.city

class Asesor(models.Model):
    """"""
    name = models.CharField(max_length=100)
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursale, on_delete=models.CASCADE)
    cooviahorro = models.CharField(max_length=500, default="0")

    def __str__(self) -> str:
        return f"{self.name} - {self.rol}"

    class Meta:
        ordering = ['id']

class File(models.Model):
    """"""
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    fileComisiones = models.FileField(upload_to='uploads/', default="emptycomisiones.xlsx")
    fileAhorroVista = models.FileField(upload_to='uploads/', default="emptyahorro.xlsx")
    fileCrecimientoBase = models.FileField(upload_to='uploads', default="empty.xlsx")
    fileCrecimientoCDAT = models.FileField(upload_to='uploads', default="emptyCrecimientoBase.xlsx")
    created = models.DateField(auto_now_add=True) 
    
    @property
    def full_date(self):
        return f"{self.month:02d}-{self.year}"
    
    def __str__(self):
        return f"Archivo {self.full_date}"
    
    class Meta:
        ordering = ['-created']


class CooviahorroMonth(models.Model):
    """"""
    nameAsesor = models.CharField(max_length=100)
    totalValue = models.CharField(max_length=100)
    year = models.IntegerField()
    month = models.IntegerField()
    court = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.nameAsesor} con {self.totalValue} del {self.month}/{self.year}"
    
    class Meta:
        ordering = ['-year', '-month']

class Court(models.Model):
    """"""
    value = models.IntegerField()
    
    def __str__(self):
        """"""
        return f"Numero de meses de corte: {self.value}"