from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

@login_required
def controlTasas(request):
    """"""
    return render(request, 'control.html')

@login_required
def afiliacionesView(request):
    afiliaciones = Afiliaciones.objects.all()
    form = AfiliacionesForm()
    if request.method == 'POST':
        form = AfiliacionesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('afiliaciones')
    return render(request, 'tasas/afiliaciones.html', {
        'form': form,
        'afiliaciones': afiliaciones
    })

@login_required
def colocaciones(request):
    col = Colocaciones.objects.all()
    form = ColocacionesForm()
    if request.method == 'POST':
        form = ColocacionesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('colocaciones')
    return render(request, 'tasas/colocaciones.html', {
        'form': form,
        'colocaciones': col
    })

@login_required
def cooviahorro(request):
    cooviahorros = Cooviahorro.objects.all()
    form = ColocacionesForm()
    if request.method == 'POST':
        form = ColocacionesForm(request.POST)
        if form.is_valid():
            return redirect('cooviahorro')
    return render(request, 'tasas/cooviahorro.html', {
        'form': form,
        'cooviahorros': cooviahorros
    })

@login_required
def cdat(request):
    cdats = Cdat.objects.all()
    form = CdatForm()
    if request.method == 'POST':
        form = CdatForm(request.POST)
        if form.is_valid():
            return redirect('cdats')
    return render(request, 'tasas/cdats.html', {
        'form': form,
        'cdats': cdats
    })

@login_required
def cdatTasas(request):
    cdatsTasas = CdatTasas.objects.all()
    form = CdatTasasForm()
    if request.method == 'POST':
        form = CdatTasasForm(request.POST)
        if form.is_valid():
            return redirect('cdatsTasas')
    return render(request, 'tasas/cdatstasas.html', {
        'form': form,
        'cdatsTasas': cdatsTasas
    })

@login_required
def ahorroVista(request):
    ahorros = AhorroVista.objects.all()
    form = AhorroVistaForm()
    if request.method == 'POST':
        form = AhorroVistaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ahorros')
    return render(request, 'tasas/ahorrosVista.html',{
        'form': form,
        'ahorros': ahorros
    })

@login_required
def crecimientoBase(request):
    crecimientoBase = CrecimientoBaseSocial.objects.all()
    form = CrecimientoBaseSocialForm()
    if request.method == 'POST':
        form = CrecimientoBaseSocialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crecimientoBase')
    return render(request, 'tasas/crecimientoBase.html', {
        'form': form,
        'crecimientoBase': crecimientoBase
    })

@login_required
def crecimientoCDAT(request):
    crecimientoCdat = CrecimientoCDAT.objects.all()
    form = CrecimientoCDATForm()
    if request.method == 'POST':
        form = CrecimientoCDATForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crecimientoCdat')
    return render(request, 'tasas/crecimientoCdat.html',{
        'form': form,
        'crecimientoCdat': crecimientoCdat
    })

@login_required
def crecimientoCoovi(request):
    crecimientoCoovi = CrecimientoCooviahorro.objects.all()
    form = CrecimientoCooviahorroForm()
    if request.method == 'POST':
        form = CrecimientoCooviahorroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crecimientoCooviahorro')
    return render(request, 'tasas/crecimientoCooviahorro.html', {
        'form': form,
        'crecimientoCoovi': crecimientoCoovi
    })

@login_required
def crecimientoAhorroVista(request):
    crecimientoAhorro = CrecimientoAhorroVista.objects.all()
    form = CrecimientoAhorroVistaForm()
    if request.method == 'POST':
        form = CrecimientoAhorroVistaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crecimientoAhorro')
    return render(request, 'tasas/crecimientoAhorroVista.html', {
        'form': form,
        'crecimientoAhorro': crecimientoAhorro
    })

@login_required
def crecimientoCartera(request):
    cartera = CrecimientoCartera.objects.all()
    form = CrecimientoCarteraForm()
    if request.method == "POST":
        form = CrecimientoCarteraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crecimientoCartera")
    return render(request, "tasas/crecimientoCartera.html", {
        "form": form,
        "carteras": cartera
    })