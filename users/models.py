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
    
class Subzona(models.Model):
    """"""
    subzona = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.subzona

class Asesor(models.Model):
    """"""
    name = models.CharField(max_length=100)
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursale, on_delete=models.CASCADE)
    subzona = models.ForeignKey(Subzona, on_delete=models.CASCADE, null=True)
    cooviahorro = models.CharField(max_length=500, default="0")

    def __str__(self) -> str:
        return f"{self.name} - {self.rol}"

    class Meta:
        ordering = ['name']

class File(models.Model):
    """"""
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    fileComisiones = models.FileField(upload_to='uploads/', default="emptycomisiones.xlsx")
    fileAhorroVista = models.FileField(upload_to='uploads/', default="emptyahorro.xlsx")
    fileCrecimientoBase = models.FileField(upload_to='uploads', default="empty.xlsx")
    fileCrecimientoCDAT = models.FileField(upload_to='uploads', default="emptyCrecimientoBase.xlsx")
    fileCrecimientoCooviahorro = models.FileField(upload_to='uploads', default="emptyCrecimientoCooviahorro.xlsx")
    fileCrecimientoAhorro = models.FileField(upload_to='uploads', default="emptyCrecimientoAhorro.xlsx")
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

class CountCrecimientoCDAT(models.Model):
    """"""
    value = models.IntegerField()
    
    def __str__(self):
        return f"Numero de registros de cdat para tener en cuenta, {self.value}"

class CrecimientoCdatMonth(models.Model):
    """"""
    name = models.ForeignKey(Sucursale, on_delete=models.CASCADE)
    value = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    
    def __str__(self):
        return f"Crecimiento CDAT en {self.name}, valor: {self.value} en el mes de {self.month} del año {self.year}"
    
    class Meta:
        ordering = ['-year', '-month']

class CrecimientoCooviahorroMonth(models.Model):
    """"""
    name = models.ForeignKey(Sucursale, on_delete=models.CASCADE)
    value = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    
    def __str__(self):
        return f"Crecimiento de Cooviahorro de {self.value} el {self.year}/{self.month}"
    
    class Meta:
        ordering = ['-year', '-month']

class CountCrecimientoCooviahorro(models.Model):
    """"""
    value = models.IntegerField()
    
    def __str__(self):
        return f"Numero de registros de crecimiento de cooviahorros para tener en cuenta, {self.value}"

class CrecimientoCarteraMonth(models.Model):
    """"""
    name = models.ForeignKey(Sucursale, on_delete=models.CASCADE)
    value = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    
    def __str__(self):
        return f"Crecimiento de Cartera de {self.value} el {self.year}/{self.month}"
    
    class Meta:
        ordering = ['-year', '-month']