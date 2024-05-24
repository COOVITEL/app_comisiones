from django.shortcuts import render
from .functions import afiliaciones, colocaciones, cooviahorro
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
            "cooviahorros": cooviahorro(name, current_file)
            #"colocaiones": readExcel(name, "Desembolsos", "NNPROMOT", ["A_OBLIGA", "CODNOMINA", "NOMINA", "MONTO", "CARTERA", "NETO_ANTES", "P_TASEFEC", "NNPROMOT", "F_CORTE", "SUC_PRODUCTO"]),
            #"cdats": readExcel(name, "CDAT", "PROMOTOR", ["CC", "A_TITULO", "Q_PLADIA", "V_TITULO", "M_ANTERIOR", "T_EFECTIVA", "PROMOTOR", "F_CORTE", "SUC_PRODUCTO"]),
            #"cooviahorros": readExcel(name, "Cooviahorro", "PROMOTOR", ["NNASOCIA", "CODNOMINA", "V_CUOTA", "SALDO", "PROMOTOR", "F_CORTE", "SUC_PRODUCTO"]),
            #"rotativo": readExcel(name, "Rotativos", ["A_NUMNIT", "N_NOMBRE", "CODNOMINA", "NOMINA", "N_MODALI", "A_OBLIGA", "SUMA_UTL", "F_CORTE", "SUC_PRODUCTO"]),
            #"ahorros": readExcel(name, "Ah Vista", "PROMOTOR", ["COD_INTERNO", "NNASOCIA", "CODNOMINA", "NOMINA", "SALDO", "PROMOTOR", "F_CORTE", "SUC_PRODUCTO"])
        }
    return render(request, "comisiones.html", dates)

