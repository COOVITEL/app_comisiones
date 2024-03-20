from django.urls import path
from . import views

urlpatterns = [
    path("asesores/", views.asesores, name="asesores"),
    path("sucursales/", views.sucursales, name="sucursales"),
    path("deleteasesor/<int:id>", views.deleteasesor, name="deleteasesor"),
    path("deletesucursal/<int:id>", views.deleteSucursal, name="deletesucursal"),
    path("comisiones/<str:name>/", views.comisiones, name="comisionesAsesor"),
    path("files/", views.files, name="files"),
    path("list_files/", views.optionsFiles, name="list_files"),
    path("list_files/<str:file>/", views.optionsAsesors, name="list_asesor")
]