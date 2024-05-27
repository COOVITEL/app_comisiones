from django.shortcuts import render
from .functions import afiliaciones, colocaciones, cooviahorro, cdats
from users.models import File, Asesor

def comisiones(request, name, file):
    """"""
    month, year = file.split('-')
    current_file = File.objects.get(month=month, year=year)
    dates = {
            "file": file,
            "asesor": name,
            "afiliaciones": afiliaciones(name, current_file),
            "colocaciones": colocaciones(name, current_file),
            "cooviahorros": cooviahorro(name, current_file),
            "cdats": cdats(name, current_file),
            #"cooviahorros": readExcel(name, "Cooviahorro", "PROMOTOR", ["NNASOCIA", "CODNOMINA", "V_CUOTA", "SALDO", "PROMOTOR", "F_CORTE", "SUC_PRODUCTO"]),
            #"rotativo": readExcel(name, "Rotativos", ["A_NUMNIT", "N_NOMBRE", "CODNOMINA", "NOMINA", "N_MODALI", "A_OBLIGA", "SUMA_UTL", "F_CORTE", "SUC_PRODUCTO"]),
            #"ahorros": readExcel(name, "Ah Vista", "PROMOTOR", ["COD_INTERNO", "NNASOCIA", "CODNOMINA", "NOMINA", "SALDO", "PROMOTOR", "F_CORTE", "SUC_PRODUCTO"])
        }
    return render(request, "comisiones.html", dates)

