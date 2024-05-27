from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Afiliaciones, Colocaciones, Cooviahorro, Cdat
from .forms import AfiliacionesForm, ColocacionesForm, CooviahorroForm, CdatForm

@login_required
def controlTasas(request):
    """"""
    list_afiliaciones = Afiliaciones.objects.all()
    colocaciones = Colocaciones.objects.all()
    cooviahorro = Cooviahorro.objects.all()
    cdats = Cdat.objects.all()
    formAfi = AfiliacionesForm()
    formCol = ColocacionesForm()
    formCoovi = CooviahorroForm()
    formCdat = CdatForm()
    if request.method == "POST":
        formAfi = AfiliacionesForm(request.POST)
        formCol = ColocacionesForm(request.POST)
        formCoovi = CooviahorroForm(request.POST)
        formCdat = CdatForm(request.POST)
        if formAfi.is_valid():
            formAfi.save()
            return redirect('tasas')
        if formCol.is_valid():
            formCol.save()
            return redirect('tasas')
        if formCoovi.is_valid():
            formCoovi.save()
            return redirect('tasas')
        if formCdat.is_valid():
            formCdat.save()
            return redirect('tasas')
    return render(request, 'control.html',
                  {'afiliaciones': list_afiliaciones,
                    'col': colocaciones,
                    'coovi': cooviahorro,
                    'cdats': cdats,
                    'formAfi': formAfi,
                    'formCol': formCol,
                    'formCoovi': formCoovi,
                    'formCdat': formCdat})
    