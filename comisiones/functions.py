from users.models import File
from .read_excel import readExcel
from tasas.models import Afiliaciones, Colocaciones
from users.models import Asesor

def afiliaciones(name, current_file):
    """
    """
    afiliaciones = readExcel(name,
                             "Afiliaciones",
                             "PROMOTOR",
                             ["NOMBRES", "COD_INTERNO", "CODNOMINA", "NOMINA", "PROMOTOR", "F_CORTE", "SUCURSAL"],
                             current_file.file)
    numberAfiliaciones = len(afiliaciones)
    tasasAfiliaciones = Afiliaciones.objects.all()
    # Inicializa tasa con None o cualquier otro valor predeterminado adecuado
    tasa = None

    for tasas in tasasAfiliaciones:
        if numberAfiliaciones >= tasas.since and numberAfiliaciones <= tasas.until:
            tasa = tasas
            break
    
    afiliaciones = {
        "afiliaciones": afiliaciones,
        "numberAfiliaciones": numberAfiliaciones,
        "tasas": tasa,
        "pagoAfiliaciones": int(numberAfiliaciones) * int(tasa.value) if tasa else 0,  # Asegura que pagoAfiliaciones maneje correctamente el caso cuando tasa es None
    }
    return afiliaciones


def colocaciones(name, current_file):
    """"""
    col = Colocaciones.objects.all()
    asesor = Asesor.objects.get(name=name)
    print(asesor.name)
    colocaciones = readExcel(name,
                             "Desembolsos",
                             "NNPROMOT",
                             ["A_OBLIGA", "NOMINA", "MONTO", "CARTERA", "NETO_ANTES", "P_TASEFEC", "NNPROMOT", "F_CORTE", "SUC_PRODUCTO"],
                             current_file.file
                             )
    setColocaciones = [
        {**d,
            'NETO_ANTES': str(d['NETO_ANTES']).split(".")[0],
            'MONTO': str(d['MONTO']).split(".")[0],
            'CARTERA': str(d['CARTERA']).split(".")[0]
        }
        for d in colocaciones]
    
    values = sum(int(value["NETO_ANTES"]) for value in setColocaciones)
    
    filterCol = [c for c in col if int(values) >= int(c.value_min) and int(values) <= int(c.value_max) and str(asesor.rol) == str(c.rol)]
    
    comision = 0
    for col in setColocaciones:
        tasaMonth = float(col['P_TASEFEC'] / 12)
        for filtC in filterCol:
            if tasaMonth >= float(filtC.tasa_min) and tasaMonth <= float(filtC.tasa_max):        
                comision += int(filtC.value)
    colocations = {
        "colocaciones": setColocaciones,
        "neto": values,
        "tasa": setColocaciones,
        "comision": comision
    }
    
    return colocations
