from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Asesor, Sucursale
from .read_excel import readExcel

@login_required
def asesores(request):
    """"""
    permission = False
    if request.user.is_superuser:
        permission = True
    citys = Sucursale.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        city = request.POST['sucursal']
        sucursal = Sucursale.objects.get(city=city)
        create = Asesor(name=name, sucursal=sucursal)
        create.save()
        return redirect("asesores")

    ciudad = Sucursale.objects.all()
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
                                                   "permission": permission,
                                                   "citys": citys})


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
    citys = Sucursale.objects.all()
    return render(request, "users/sucursales.html",
                            {"citys": citys,
                             "permission": user_permissions})

@login_required
def createsucursal(request):
    """"""
    if request.method == "POST":
        city = request.POST['city']
        create = Sucursale(city=city)
        create.save()
        return redirect("sucursales")
    return render(request, "users/createsucursal.html")

@login_required
def deleteSucursal(request, id):
    """"""
    sucursal = Sucursale.objects.get(id=id)
    sucursal.delete()
    return redirect("sucursales")

@login_required
def comisiones(request, name):
    """"""
    dates = {}
    dates = {"asesor": Asesor.objects.get(name=name),
            "afiliaciones": readExcel(name, "Afiliaciones", "PROMOTOR", ["COD_INTERNO", "CODNOMINA", "NOMINA", "PROMOTOR", "F_CORTE", "SUCURSAL"]),
            #"colocaiones": readExcel(name, "Desembolsos", "NNPROMOT", ["A_OBLIGA", "CODNOMINA", "NOMINA", "MONTO", "CARTERA", "NETO_ANTES", "P_TASEFEC", "NNPROMOT", "F_CORTE", "SUC_PRODUCTO"]),
            "cdats": readExcel(name, "CDAT", "PROMOTOR", ["CC", "A_TITULO", "Q_PLADIA", "V_TITULO", "M_ANTERIOR", "T_EFECTIVA", "PROMOTOR", "F_CORTE", "SUC_PRODUCTO"]),
            "cooviahorros": readExcel(name, "Cooviahorro", "PROMOTOR", ["NNASOCIA", "CODNOMINA", "V_CUOTA", "SALDO", "PROMOTOR", "F_CORTE", "SUC_PRODUCTO"]),
            #"rotativo": readExcel(name, "Rotativos", ["A_NUMNIT", "N_NOMBRE", "CODNOMINA", "NOMINA", "N_MODALI", "A_OBLIGA", "SUMA_UTL", "F_CORTE", "SUC_PRODUCTO"]),
            "ahorros": readExcel(name, "Ah Vista", "PROMOTOR", ["COD_INTERNO", "NNASOCIA", "CODNOMINA", "NOMINA", "SALDO", "PROMOTOR", "F_CORTE", "SUC_PRODUCTO"])
        }
    return render(request, "users/comisiones.html", dates)