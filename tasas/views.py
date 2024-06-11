from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Afiliaciones, Colocaciones, Cooviahorro, Cdat, CdatTasas, AhorroVista, CrecimientoBaseSocial
from .forms import AfiliacionesForm, ColocacionesForm, CooviahorroForm, CdatForm, CdatTasasForm, AhorroVistaForm, CrecimientoBaseSocialForm

@login_required
def controlTasas(request):
    """"""
    list_afiliaciones = Afiliaciones.objects.all()
    colocaciones = Colocaciones.objects.all()
    cooviahorro = Cooviahorro.objects.all()
    cdats = Cdat.objects.all()
    cdatstasas = CdatTasas.objects.all()
    ahorros = AhorroVista.objects.all()
    crecimeintoBase = CrecimientoBaseSocial.objects.all()
    
    formAfi = AfiliacionesForm()
    formCol = ColocacionesForm()
    formCoovi = CooviahorroForm()
    formCdat = CdatForm()
    formCdatTasas = CdatTasasForm()
    formAhorro = AhorroVistaForm()
    formCrecimientoBase = CrecimientoBaseSocialForm()
    
    if request.method == "POST":
        formAfi = AfiliacionesForm(request.POST)
        formCol = ColocacionesForm(request.POST)
        formCoovi = CooviahorroForm(request.POST)
        formCdat = CdatForm(request.POST)
        formCdatTasas = CdatTasasForm(request.POST)
        formAhorro = AhorroVistaForm(request.POST)
        formCrecimientoBase = CrecimientoBaseSocialForm(request.POST)
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
        if formCdatTasas.is_valid():
            formCdatTasas.save()
            return redirect('tasas')
        if formAhorro.is_valid():
            formAhorro.save()
            return redirect('tasas')
        if formCrecimientoBase.is_valid():
            formCrecimientoBase.save()
            return redirect('tasas')

    return render(request, 'control.html',
                  {'afiliaciones': list_afiliaciones,
                    'col': colocaciones,
                    'coovi': cooviahorro,
                    'cdats': cdats,
                    'cdatstasas': cdatstasas,
                    'ahorros': ahorros,
                    'crecimientoBase': crecimeintoBase,
                    'formAfi': formAfi,
                    'formCol': formCol,
                    'formCoovi': formCoovi,
                    'formCdat': formCdat,
                    'formCdatTasas': formCdatTasas,
                    'formAhorro': formAhorro,
                    'formCrecimientoBase': formCrecimientoBase
                    })

