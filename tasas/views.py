from django.shortcuts import render, redirect
from .models import Afiliaciones
from .forms import AfiliacionesForm

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

def afiliaciones(request):
    """"""
    return render(request, 'tasas/afiliaciones.html')