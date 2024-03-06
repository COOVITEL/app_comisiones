from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Asesor, Sucursales
import pandas as pd
import os

@login_required
def asesores(request):
    """"""
    permission = False
    if request.user.is_superuser:
        permission = True
    ciudad = Sucursales.objects.all()
    city = request.GET.get("ciudad", None)
    todos = request.GET.get("todos", None)
    if todos is not None:
        asesores = Asesor.objects.all()
    elif city is None or city == "":
        asesores = Asesor.objects.all()
    else:
        asesores = Asesor.objects.filter(sucursal__city=city)
    return render(request, "users/asesores.html", {"asesores": asesores,
                                                   "ciudades": ciudad,
                                                   "permission": permission})

@login_required
def createasesor(request):
    """"""
    citys = Sucursales.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        city = request.POST['sucursal']
        sucursal = Sucursales.objects.get(city=city)
        create = Asesor(name=name, sucursal=sucursal)
        create.save()
        return redirect("asesores")
    return render(request, 'users/createasesor.html', {"citys": citys})

@login_required
def deleteasesor(request, id):
    """"""
    asesor = Asesor.objects.get(id=id)
    asesor.delete()
    return redirect('asesores')

@login_required
def sucursales(request):
    """"""
    user_permissions = False
    if request.user.is_superuser:
        user_permissions = True
    citys = Sucursales.objects.all()
    return render(request, "users/sucursales.html",
                            {"citys": citys,
                             "permission": user_permissions})

@login_required
def createsucursal(request):
    """"""
    if request.method == "POST":
        city = request.POST['city']
        create = Sucursales(city=city)
        create.save()
        return redirect("sucursales")
    return render(request, "users/createsucursal.html")

@login_required
def deleteSucursal(request, id):
    """"""
    sucursal = Sucursales.objects.get(id=id)
    sucursal.delete()
    return redirect("sucursales")
