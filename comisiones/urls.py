from django.urls import path
from . import views

urlpatterns = [
    path("<str:name>/<str:file>/", views.comisiones, name="comisionesAsesor"),    
]