from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Afiliaciones
from .forms import AfiliacionesForm

@login_required
def controlTasas(request):
    """"""
    list_afiliaciones = Afiliaciones.objects.all()
    form = AfiliacionesForm()
    if request.method == "POST":
        form = AfiliacionesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasas')
    
    return render(request, 'control.html',
                  {'afiliaciones': list_afiliaciones,
                   'form': form})

@login_required
def afiliaciones(request):
    """"""
    return render(request, 'tasas/afiliaciones.html')