from django.db import models

class Roles(models.Model):
    """"""
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name