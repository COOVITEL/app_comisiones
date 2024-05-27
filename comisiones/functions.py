from users.models import File
from .read_excel import readExcel
from tasas.models import Afiliaciones, Colocaciones, Cooviahorro
from users.models import Asesor, CooviahorroMonth, Court
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
        
        for filtC in filterCol:
            if tasaNominal >= float(filtC.tasa_min) and tasaNominal <= float(filtC.tasa_max):        
                currentComision = math.ceil((int(filtC.value) * numero))
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
    comisionValue = coovi[0].value.replace(".", "")
    comisionMonto = coovi[0].monto.replace(".", "")
    currentCourt = Court.objects.all()[0].value
    cooviahorros = readExcel(name,
                             "Cooviahorro",
                             "PROMOTOR",
                             ["AANUMNIT", "K_NUMDOC", "N_TIPODR", "SALDO", "PROMOTOR"],
                             current_file.file)
    setCooviahorros = [
        {**d,
            'SALDO': str(d['SALDO']).split(".")[0],
        }
        for d in cooviahorros]
    
    monto = sum(int(value['SALDO']) for value in setCooviahorros)
    date = str(current_file).split("-")
    month = date[0]
    year = date[1]
    
    if not CooviahorroMonth.objects.filter(nameAsesor=name, year=year, month=month).exists():
        registerCoovi = CooviahorroMonth(nameAsesor=name, totalValue=monto, year=year, month=month, court=currentCourt)
        registerCoovi.save()
    
    asesorHistory = CooviahorroMonth.objects.filter(nameAsesor=name)
    
    controlState = False
    controlPosition = 0
    value = 0
    for historyDate in asesorHistory:
        if int(historyDate.totalValue) == int(monto):
            controlState = True
            corte = historyDate.court
            continue
        if controlState:
            controlPosition += 1
            if int(historyDate.totalValue) > value:
                value = int(historyDate.totalValue)
            if controlPosition > int(corte):
                break
    
    totalMonto = int(monto) - int(value)

    comision = math.ceil((totalMonto / int(comisionMonto)) * int(comisionValue))
    listCooviahorros = {
        'cooviahorros': setCooviahorros,
        'monto': totalMonto,
        'comision': comision
    }
    return listCooviahorros

def cdats(name, current_file):
    """"""
    date = str(current_file).split("-")
    currentDate = f"{date[1]}-{date[0]}"
    cdats = readExcel(name,
                             "Cdat",
                             "PROMOTOR",
                             ["K_IDTERC", "NOMBRE_TERCERO", "V_TITULO", "F_TITULO", "Q_PLADIA", "M_ANTERIOR", "T_NOMINAL", "RETENCION", "PROMOTOR"],
                             current_file.file)

    setListCdats = [cdat for cdat in cdats if str(str(cdat['F_TITULO']).split(" ")[0])[:-3] == currentDate]

    setCdats = [
        {**d,
            'V_TITULO': str(d['V_TITULO']).split(".")[0],
            'M_ANTERIOR': str(d['M_ANTERIOR']).split(".")[0],
            'Q_PLADIA': str(d['Q_PLADIA']).split(".")[0],
            'V_NUEVO': int(str(d['V_TITULO']).split(".")[0]) - int(str(d['M_ANTERIOR']).split(".")[0]),
            'FACTOR_PLAZO': round(int(d['Q_PLADIA']) / 360, 2)
        }
        for d in setListCdats]
    
    totalNuevo = sum(int(value['V_NUEVO']) for value in setCdats)
    totalRenovado = sum(int(value['M_ANTERIOR']) for value in setCdats)

    listCdats = {
        'cdats': setCdats,
        'totalNuevo': totalNuevo,
        'totalRenovado': totalRenovado
    }

    return listCdats