from django.urls import path
from . import views

urlpatterns = [
    path('', views.roles, name="roles"),
    path('eliminar_rol/<int:id>/', views.deleteRole, name="delete_rol"),
]