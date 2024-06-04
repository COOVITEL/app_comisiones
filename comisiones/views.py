from django.shortcuts import render
from .functions import afiliaciones, colocaciones, cooviahorro, cdats, ahorroVista
from users.models import File, Asesor

def comisiones(request, name, file):
    """"""
    month, year = file.split('-')
    current_file = File.objects.get(month=month, year=year)
    archivoComisiones = current_file.fileComisiones
    archivoAhorriVista = current_file.fileAhorroVista
    dates = {
            "file": file,
            "asesor": name,
            # "afiliaciones": afiliaciones(name, archivoComisiones),
            # "colocaciones": colocaciones(name, archivoComisiones),
            # "cooviahorros": cooviahorro(name, archivoComisiones, file),
            # "cdats": cdats(name, archivoComisiones, file),
            "ahorrosVista": ahorroVista(name, archivoAhorriVista)
            #"rotativo": readExcel(name, "Rotativos", ["A_NUMNIT", "N_NOMBRE", "CODNOMINA", "NOMINA", "N_MODALI", "A_OBLIGA", "SUMA_UTL", "F_CORTE", "SUC_PRODUCTO"]),
            #"ahorros": readExcel(name, "Ah Vista", "PROMOTOR", ["COD_INTERNO", "NNASOCIA", "CODNOMINA", "NOMINA", "SALDO", "PROMOTOR", "F_CORTE", "SUC_PRODUCTO"])
        }
    return render(request, "comisiones.html", dates)

