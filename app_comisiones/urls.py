from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('registros/', include('users.urls')),
    path('roles/', include('roles.urls')),
    path('control_de_comisiones/', include('tasas.urls')),
    path('comisiones/', include('comisiones.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)