from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Asesor, Sucursale

def dashboard(request):
    asesors = Asesor.objects.count()
    sucursales = Sucursale.objects.count()
    return render(request, 'account/dashboard.html',
                  {'section': 'dashboard',
                   'asesors': asesors,
                   'sucursales': sucursales})

