from django.db import models

MONTH_CHOICES = [(i, i) for i in range(1, 13)]
YEAR_CHOICES = [(i, i) for i in range(2023, 2040)]

class Sucursale(models.Model):
    """"""
    city = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.city

class Asesor(models.Model):
    """"""
    name = models.CharField(max_length=100)
    sucursal = models.ForeignKey(Sucursale, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class File(models.Model):
    """"""
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    file = models.FileField(upload_to='uploads/')
    
    @property
    def full_date(self):
        return f"{self.year}-{self.month:02d}"
    
    def __str__(self):
        return self.full_date