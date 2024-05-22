from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Afiliaciones, Colocaciones
from .forms import AfiliacionesForm, ColocacionesForm

@login_required
def controlTasas(request):
    """"""
    list_afiliaciones = Afiliaciones.objects.all()
    colocaciones = Colocaciones.objects.all()
    formAfi = AfiliacionesForm()
    formCol = ColocacionesForm()
    if request.method == "POST":
        formAfi = AfiliacionesForm(request.POST)
        formCol = ColocacionesForm(request.POST)
        if formAfi.is_valid():
            formAfi.save()
            return redirect('tasas')
        if formCol.is_valid():
            formCol.save()
            return redirect('tasas')
    return render(request, 'control.html',
                  {'afiliaciones': list_afiliaciones,
                   'col': colocaciones,
                  'formAfi': formAfi,
                   'formCol': formCol})
    