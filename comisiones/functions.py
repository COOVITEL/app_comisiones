from users.models import File
from .read_excel import readExcel
from tasas.models import Afiliaciones

def afiliaciones(name, current_file):
    """"""
    afiliaciones = readExcel(name,
                             "Afiliaciones",
                             "PROMOTOR",
                             ["NOMBRES", "COD_INTERNO", "CODNOMINA", "NOMINA", "PROMOTOR", "F_CORTE", "SUCURSAL"],
                             current_file.file)
    numberAfiliaciones = len(afiliaciones)
    tasasAfiliaciones = Afiliaciones.objects.all()

    for tasas in tasasAfiliaciones:
        if numberAfiliaciones >= tasas.since and numberAfiliaciones <= tasas.until:
            tasa = tasas
            break
    afiliaciones = {
        "afiliaciones": afiliaciones,
        "numberAfiliaciones": numberAfiliaciones,
        "tasas": tasa,
        "pagoAfiliaciones": int(numberAfiliaciones) * int(tasa.value),
    }
    return afiliaciones

def colocaciones(name, current_file):
    """"""
    colocaciones = readExcel(name,
                             "Desembolsos",
                             "NNPROMOT",
                             ["A_OBLIGA", "CODNOMINA", "NOMINA", "MONTO", "CARTERA", "NETO_ANTES", "P_TASEFEC", "NNPROMOT", "F_CORTE", "SUC_PRODUCTO"],
                             current_file.file
                             )
    colocations = {
        "colocaciones": colocaciones
    }
    return colocations
