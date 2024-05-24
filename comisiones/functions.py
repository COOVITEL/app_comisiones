from users.models import File
from .read_excel import readExcel
from tasas.models import Afiliaciones, Colocaciones, Cooviahorro
from users.models import Asesor
import math

def afiliaciones(name, current_file):
    """
    """
    afiliaciones = readExcel(name,
                             "Afiliaciones",
                             "PROMOTOR",
                             ["NOMBRES", "COD_INTERNO", "CODNOMINA", "NOMINA", "ACUM_APO", "ACUM_AHO", "PROMOTOR", "F_CORTE", "SUCURSAL"],
                             current_file.file)
    
    setAfiliaciones = [afi for afi in afiliaciones if afi["ACUM_AHO"] > 0]
    numberAfiliaciones = len(setAfiliaciones)
    tasasAfiliaciones = Afiliaciones.objects.all()
    # Inicializa tasa con None o cualquier otro valor predeterminado adecuado
    tasa = None

    for tasas in tasasAfiliaciones:
        if numberAfiliaciones >= tasas.since and numberAfiliaciones <= tasas.until:
            tasa = tasas
            break
    
    afiliaciones = {
        "afiliaciones": setAfiliaciones,
        "numberAfiliaciones": numberAfiliaciones,
        "tasas": tasa,
        "pagoAfiliaciones": int(numberAfiliaciones) * int(tasa.value) if tasa else 0,  # Asegura que pagoAfiliaciones maneje correctamente el caso cuando tasa es None
    }
    return afiliaciones


def colocaciones(name, current_file):
    """"""
    col = Colocaciones.objects.all()
    asesor = Asesor.objects.get(name=name)
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
        number = int(col["NETO_ANTES"])
        numero = number / 1000000
        
        tasa = float(col["P_TASEFEC"]) / int(100)
        tasaNominal = ((12 * ((1 + tasa)**(1/12) - 1)) / 12) * 100
        
        print(f"Monto {col['NETO_ANTES']}")
        print(f"Tasa Anual {tasa}")
        print(f"Tasa Nominal {tasaNominal}")
        print(f"Numero {numero}")
        for filtC in filterCol:
            if tasaNominal >= float(filtC.tasa_min) and tasaNominal <= float(filtC.tasa_max):        
                print(f"Cantidad de pago {filtC.value}")
                currentComision = math.ceil((int(filtC.value) * numero))
                print(f"Comision {currentComision}")
                print()
                comision += int(str(currentComision).split(".")[0])
    colocations = {
        "colocaciones": setColocaciones,
        "neto": values,
        "tasa": setColocaciones,
        "comision": comision
    }
    
    return colocations

def cooviahorro(name, current_file):
    coovi = Cooviahorro.objects.all()
    currentMonto = int(coovi[0].monto.replace(".", ""))
    currentValue = int(coovi[0].value.replace(".", ""))
    cooviahorros = readExcel(name,
                             "Cooviahorro",
                             "PROMOTOR_ANT",
                             ["AANUMNIT", "K_NUMDOC", "N_TIPODR", "SALDO", "PROMOTOR_ANT"],
                             current_file.file)
    setCooviahorros = [
        {**d,
            'SALDO': str(d['SALDO']).split(".")[0],
        }
        for d in cooviahorros]
    monto = sum(int(value['SALDO']) for value in setCooviahorros)
    numbersComisions = int(monto / int(currentMonto))
    comision = numbersComisions * int(currentValue)
    listCooviahorros = {
        'cooviahorros': setCooviahorros,
        'monto': monto,
        'comision': comision
    }
    return listCooviahorros