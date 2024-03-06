from django.urls import path
from . import views

urlpatterns = [
    path("asesores/", views.asesores, name="asesores"),
    path("sucursales/", views.sucursales, name="sucursales"),
    path("createsucursal/", views.createsucursal, name="createsucursal"),
    path("deleteasesor/<int:id>", views.deleteasesor, name="deleteasesor"),
    path("deletesucursal/<int:id>", views.deleteSucursal, name="deletesucursal"),
    path("comisiones/<str:name>", views.comisiones, name="comisionesAsesor"),
]