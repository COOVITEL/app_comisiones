from django.urls import path
from . import views

urlpatterns = [
    path("asesores/", views.asesores, name="asesores"),
    path("sucursales/", views.sucursales, name="sucursales"),
    path("subzonas/", views.subzona, name="subzonas"),
    path("deleteasesor/<int:id>", views.deleteasesor, name="deleteasesor"),
    path("deletesucursal/<int:id>", views.deleteSucursal, name="deletesucursal"),
    path("deletesubzona/<int:id>", views.deleteSubzona, name="deletesubzona"),
    path("files/", views.files, name="files"),
    path("list_files/", views.optionsFiles, name="list_files"),
    path("list_files/<str:file>/", views.optionsAsesors, name="list_asesor"),
]