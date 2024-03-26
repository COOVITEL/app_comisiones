from users.models import File
from .read_excel import readExcel
from tasas.models import Afiliaciones

def afiliaciones(name, file):
    """"""
    month, year = file.split('-')
    current_file = File.objects.get(month=month, year=year)

    afiliaciones = readExcel(name, "Afiliaciones", "PROMOTOR", ["NOMBRES", "COD_INTERNO", "CODNOMINA", "NOMINA", "PROMOTOR", "F_CORTE", "SUCURSAL"], current_file.file)
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