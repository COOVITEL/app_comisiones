from django.urls import path
from . import views


urlpatterns = [
    path('', views.controlTasas, name='tasas'),
    path('afiliaciones/', views.afiliacionesView, name='afiliaciones'),
    path('colocaciones/', views.colocaciones, name='colocaciones'),
    path('cooviahorros/', views.cooviahorro, name='cooviahorro'),
    path('cdats/', views.cdat, name='cdats'),
    path('cdatsTasas/', views.cdatTasas, name='cdatsTasas'),
    path('ahorroVista', views.ahorroVista, name='ahorro'),
    path('crecimientoBase/', views.crecimientoBase, name='crecimientoBase'),
    path('crecimientoCDAT/', views.crecimientoCDAT, name='crecimientoCdat'),
    path('crecimientoCooviahorro/', views.crecimientoCoovi, name='crecimientoCooviahorro'),
    path('crecimientoAhorroVista/', views.crecimientoAhorroVista, name='crecimientoAhorro'),
    path('crecimientoCartera/', views.crecimientoCartera, name='crecimientoCartera'),
]