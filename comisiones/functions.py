from .read_excel import readExcel
from tasas.models import Afiliaciones, Colocaciones, Cooviahorro, Cdat, CdatTasas, AhorroVista, CrecimientoBaseSocial, CrecimientoCDAT
from users.models import *
import math

def afiliaciones(name, current_file):
    """
    """
    afiliaciones = readExcel(name,
                             "Afiliaciones",
                             "PROMOTOR",
                             ["NOMBRES", "COD_INTERNO", "CODNOMINA", "NOMINA", "ACUM_APO", "ACUM_AHO", "PROMOTOR", "F_CORTE", "SUCURSAL"],
                             current_file)
    
    setAfiliaciones = [afi for afi in afiliaciones if afi["ACUM_APO"] > 0]
    setListAfiliaciones = [
        {**d,
            'ACUM_AHO': str(d['ACUM_AHO']).split(".")[0],
            'ACUM_APO': str(d['ACUM_APO']).split(".")[0]
         }
        for d in setAfiliaciones
    ]
    numberAfiliaciones = len(setListAfiliaciones)
    tasasAfiliaciones = Afiliaciones.objects.all()
    tasa = 0

    for tasas in tasasAfiliaciones:
        if numberAfiliaciones >= tasas.since and numberAfiliaciones <= tasas.until:
            tasa = tasas.value

    afiliaciones = {
        "afiliaciones": setListAfiliaciones,
        "numberAfiliaciones": numberAfiliaciones,
        "tasas": int(tasa),
        "pagoAfiliaciones": int(numberAfiliaciones) * int(tasa) if tasa else 0,
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
                             current_file)
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


def cooviahorro(name, current_file, date):
    coovi = Cooviahorro.objects.all()
    comisionValue = coovi[0].value.replace(".", "")
    comisionMonto = coovi[0].monto.replace(".", "")
    currentCourt = Court.objects.all()[0].value
    cooviahorros = readExcel(name,
                             "Cooviahorro",
                             "PROMOTOR",
                             ["AANUMNIT", "K_NUMDOC", "N_TIPODR", "SALDO", "PROMOTOR"],
                             current_file)
    setCooviahorros = [
        {**d,
            'SALDO': str(d['SALDO']).split(".")[0],
        }
        for d in cooviahorros]
    
    monto = sum(int(value['SALDO']) for value in setCooviahorros)
    date = str(date).split("-")
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
    if comision < 0:
        comision = 0
    if totalMonto < 0:
        totalMonto = 0
    listCooviahorros = {
        'cooviahorros': setCooviahorros,
        'monto': totalMonto,
        'comision': comision
    }
    return listCooviahorros


def cdats(name, current_file, date):
    """"""
    asesor = Asesor.objects.get(name=name)
    date = str(date).split("-")
    currentDate = f"{date[1]}-{date[0]}"
    tasasCdats = CdatTasas.objects.all()
    cdats = readExcel(name,
                             "Cdat",
                             "PROMOTOR",
                             ["K_IDTERC", "NOMBRE_TERCERO", "V_TITULO", "F_TITULO", "Q_PLADIA", "M_ANTERIOR", "T_EFECTIVA", "T_NOMINAL", "RETENCION", "PROMOTOR"],
                             current_file)
    comisionNuevo = 0
    comisonRenovado = 0
    comisionTotal = 0
    setListCdats = [cdat for cdat in cdats if str(str(cdat['F_TITULO']).split(" ")[0])[:-3] == currentDate]

    setCdats = [
        {**d,
            'V_TITULO': str(d['V_TITULO']).split(".")[0],
            'M_ANTERIOR': str(d['M_ANTERIOR']).split(".")[0],
            'Q_PLADIA': str(d['Q_PLADIA']).split(".")[0],
            'V_NUEVO': int(str(d['V_TITULO']).split(".")[0]) - int(str(d['M_ANTERIOR']).split(".")[0]),
            'FACTOR_PLAZO': round(d['Q_PLADIA'] / 360, 2),
            'T_NOMINAL': round(d['T_NOMINAL'], 3),
        }
        for d in setListCdats]
    
    totalNuevo = sum(int(value['V_NUEVO']) for value in setCdats)
    totalRenovado = sum(int(value['M_ANTERIOR']) for value in setCdats)
    
    valuesCdats = Cdat.objects.all()
    
    if "Captaciones" in str(asesor.rol):
        setValuesCdats = [values for values in valuesCdats if "Captaciones" in str(values.rol)]
    else:
        setValuesCdats = [values for values in valuesCdats if "Captaciones" not in str(values.rol)]

    valueNew = 0
    valueReno = 0
    for valueCdat in setValuesCdats:
        valueMin = valueCdat.valueMin.replace(".", "")
        valueMax = valueCdat.valueMax.replace(".", "")
        if valueCdat.type == 'nuevo' and totalNuevo >= int(valueMin) and totalNuevo <= int(valueMax):
            valueNew = valueCdat.value
        if valueCdat.type == 'renovado' and totalRenovado >= int(valueMin) and totalRenovado <= int(valueMax):
            valueReno = valueCdat.value
    
    for cdats in setCdats:
        for tasas in tasasCdats:
            valorCdat = int(cdats['V_TITULO'])
            valorminTasa = int(tasas.valueMin.replace(".", ""))
            valormaxTasa = int(tasas.valueMax.replace(".", ""))
            time = int(cdats['Q_PLADIA'])
            timeMin = int(tasas.plazoMin)
            timeMax = int(tasas.plazoMax)
            if (valorCdat >= valorminTasa and valorCdat <= valormaxTasa) and (time >= timeMin and time <= timeMax):
                cdats['T_REF'] = tasas.tasa
                cdats['F_TASA'] = round(1 - (cdats['T_EFECTIVA'] - tasas.tasa), 3)
                cdats['F_TP'] = round(cdats['F_TASA'] * cdats['FACTOR_PLAZO'], 2)
                var = int(cdats['M_ANTERIOR']) / 1000000
                vaar = float(var) * int(valueReno)
                vReno = int(vaar * cdats['F_TP'])
                van = int(cdats['V_NUEVO']) / 1000000
                vaan = float(van) * int(valueNew)
                vNew = int(vaan * cdats['F_TP'])
                if vReno < 0:
                    vReno = 0
                if vNew < 0:
                    vNew = 0
                cdats['V_RENO'] = vReno
                cdats['V_NUEV'] = vNew
                continue
    
    comisionNuevo = sum(int(value['V_RENO']) for value in setCdats)
    comisonRenovado = sum(int(value['V_NUEV']) for value in setCdats)
    comisionTotal = comisionNuevo + comisonRenovado

    listCdats = {
        'cdats': setCdats,
        'totalNuevo': totalNuevo,
        'totalRenovado': totalRenovado,
        'comiReno': comisonRenovado,
        'comiNuevo': comisionNuevo,
        'total': comisionTotal
    }

    return listCdats


def ahorroVista(name, current_file):
    """"""
    ahorrosVista = AhorroVista.objects.all()
    
    ahorros = readExcel(name,
                        "Promedio",
                        "PROMOTOR",
                        ["CEDULA ASOCIADO", "CUENTA ASOCIADO", "Promedio 30 días", "PROMOTOR"],
                        current_file)
    setAhorros = [
        {
            'CEDULA': d['CEDULA ASOCIADO'],
            'CUENTA': d['CUENTA ASOCIADO'],
            'PROMEDIO': int(d['Promedio 30 días'])
        }
        for d in ahorros]
    promedio = sum(int(value['PROMEDIO']) for value in setAhorros)
    comision = 0
    for ahorro in ahorrosVista:
        if promedio >= int(ahorro.valueMin.replace(".", "")) and promedio <= int(ahorro.valueMax.replace(".", "")):
            comision = int(round(promedio * (ahorro.porcentaje / 100), 0))
    
    listAhorros = {
        'ahorrosVista': setAhorros,
        'promedio': promedio,
        'comision': comision
    }
    
    return listAhorros


def crecimientoBase(name, current_file):
    """"""
    asesor = Asesor.objects.get(name=name)
    setname = name.split(" ")
    setList = []
    comision = 0
    for word in setname:
        setList.append(word.capitalize())
    newName = " ".join(setList)
    crecimientoBase = CrecimientoBaseSocial.objects.all()[0]
    
    crecimiento = readExcel(newName,
                            "Afiliaciones Promotor",
                            "Gestor",
                            ["Gestor", "EJEC", "PPTO", "% CUMP"],
                            current_file
                            )
    setCrecimiento = [
        {
            'PROMOTOR': d['Gestor'],
            'EJECUTADO': d['EJEC'],
            'META': d['PPTO'],
            'PORCENTAJE': d['% CUMP'] * 100
        }
        for d in crecimiento]
    if str(asesor.rol) == "Director":
        if setCrecimiento[0]['PORCENTAJE'] > crecimientoBase.porcentaje:
            comision = int(crecimientoBase.value.replace(".", "")) * setCrecimiento[0]['EJECUTADO']
    
    listCrecimiento = {
        'crecimientoBase': setCrecimiento,
        'comision': comision
    }
    
    return listCrecimiento


def checkMeta(name, fileCDAT, fileCoovi, fileAhorro, fileComisiones, date):
    asesor = Asesor.objects.get(name=name)
    setname = name.split(" ")
    setList = []
    date = str(date).split("-")
    currentDate = f"{date[1]}-{date[0]}"
    for word in setname:
        setList.append(word.capitalize())
    newName = " ".join(setList)
    
    status = {
        'director': False,
        'state': False,
        'message': '',
        'porcentaje': '',
    }
    
    if "Director" in str(asesor.rol):
        status["director"] = True
    
    cdat = readExcel(newName,
                        "CDAT Promotor Abril",
                        "Gestor",
                        ["Gestor", "EJEC", "PPTO", "% CUMP"],
                        fileCDAT
                        )
    cooviahorro = readExcel(newName,
                        "Cooviahorro Promotor Abril",
                        "Gestor",
                        ["Gestor", "EJEC", "PPTO", "% CUMP"],
                        fileCoovi
                        )
    ahorroVista = readExcel(newName,
                        "Ahorro Vista Promotor Abril",
                        "Gestor",
                        ["Gestor", "EJEC", "PPTO", "% CUMP"],
                        fileAhorro
                        )
    
    if len(cdat) == 0 or len(cooviahorro) == 0 or len(ahorroVista) == 0:
        if "Director" in str(asesor.rol):
            status["message"] = f"Este mes no cumplio con el 80% de su meta mensual individual en Captaciones (Suma de CDAT, Cooviahorro y Ahorro Vista)." 
    
    ejecutados = int(cdat[0]["EJEC"]) + int(cooviahorro[0]["EJEC"]) + int(ahorroVista[0]["EJEC"])
    meta = int(cdat[0]["PPTO"]) + int(cooviahorro[0]["PPTO"]) + int(ahorroVista[0]["PPTO"])
    porcentaje = round((ejecutados / meta) * 100, 2)
    
    
    if status["director"] == True or porcentaje < 80 and str(asesor.rol) == "Director Capt":
        status["state"] = True
        status["message"] = f"Felicitaciones este mes cumplio con su meta mensual individual."
        status["porcentaje"] = f"Su porcentaje ejecutado fue: {porcentaje}"

        if str(asesor.rol) == "Director Capt":
            cdats = readExcel(name=str(asesor.subzona),
                    file="Cdat",
                    columns=["K_IDTERC", "NOMBRE_TERCERO", "V_TITULO", "F_TITULO", "Q_PLADIA", "M_ANTERIOR", "T_EFECTIVA", "T_NOMINAL", "RETENCION", "PROMOTOR", "SUBZONA", "SUC_PRODUCTO"],
                    archive=fileComisiones)
            asesorsCapt = Asesor.objects.all()
            asesorsCapt = [asesors for asesors in asesorsCapt if "Capt" in str(asesors.rol)]
            setListCdats = [dato for dato in cdats if dato.get('PROMOTOR') in [asesor.name for asesor in asesorsCapt]]
                            
            setCdatsDate = [cdat for cdat in setListCdats if str(str(cdat['F_TITULO']).split(" ")[0])[:-3] == currentDate]
            
        else:
            cdats = readExcel(name=str(asesor.sucursal),
                file="Cdat",
                asesor="SUC_PRODUCTO",
                columns=["K_IDTERC", "NOMBRE_TERCERO", "V_TITULO", "F_TITULO", "Q_PLADIA", "M_ANTERIOR", "T_EFECTIVA", "T_NOMINAL", "RETENCION", "PROMOTOR", "SUBZONA", "SUC_PRODUCTO"],
                archive=fileComisiones)
            setListCdats = cdats
            
            setCdatsDate = [cdat for cdat in setListCdats if str(str(cdat['F_TITULO']).split(" ")[0])[:-3] == currentDate]

        montoTotalCurrentMonth = sum(int(value['V_TITULO']) for value in setListCdats)
        
        if not CrecimientoCdatMonth.objects.filter(name=asesor.sucursal, year=date[1], month=date[0]).exists():
            crecimiento = CrecimientoCdatMonth(name=asesor.sucursal,
                                                value=int(montoTotalCurrentMonth),
                                                year=date[1],
                                                month=date[0])
            crecimiento.save()
        
        registers = CrecimientoCdatMonth.objects.filter(name=asesor.sucursal)
        controlRegisCdats = CountCrecimientoCDAT.objects.all()[0].value
        valueMax = 0
        control = 0
        for regis in registers:
            if control > 0:
                control += 1
                if regis.value > valueMax:
                    valueMax = regis.value
                if control >= controlRegisCdats:
                    break
            if regis.value == montoTotalCurrentMonth:
                control += 1
        crecimiento = montoTotalCurrentMonth - valueMax
        
        if crecimiento < 0:
            crecimiento = 0
            status["state"] = False
            status["message"] = f"Este mes no presento crecimiento en monto de los CDATs en su sucursal"
            status["porcentaje"] = f"Su porcentaje ejecutado fue: {porcentaje}"

        setCdats = [
            {
                **d,
                'V_TITULO': str(d['V_TITULO']).split(".")[0] if '.' in str(d['V_TITULO']) else '',
                'M_ANTERIOR': str(d['M_ANTERIOR']).split(".")[0] if '.' in str(d['M_ANTERIOR']) else '',
                'Q_PLADIA': str(d['Q_PLADIA']).split(".")[0] if '.' in str(d['Q_PLADIA']) else '',
                'V_NUEVO': int(str(d['V_TITULO']).split(".")[0]) - int(str(d['M_ANTERIOR']).split(".")[0]) if '.' in str(d['V_TITULO']) and '.' in str(d['M_ANTERIOR']) else 0,
                'FACTOR_PLAZO': round(float(d['Q_PLADIA']) / 360, 2) if '.' in str(d['Q_PLADIA']) else 0.0,
                'T_NOMINAL': round(float(d['T_NOMINAL']), 3) if isinstance(d['T_NOMINAL'], (int, float)) else 0.0,
            }
            for d in setCdatsDate]

        tasas = [value.get('T_EFECTIVA') for value in setCdatsDate]
        values = [value.get('V_TITULO') for value in setCdatsDate]
        plazos = [value.get('Q_PLADIA') for value in setCdatsDate]
        montoTotal = sum(int(value['V_TITULO']) for value in setCdatsDate)
        
        tasaPromedio = round(sum(a*b for a, b in zip(values, tasas)) / montoTotal, 2)
        plazoPromedio = round(sum(a*b for a, b in zip(values, plazos)) / montoTotal, 2)
        
        status["tasaPromedio"] = tasaPromedio
        status["plazoPromedio"] = plazoPromedio
        status["montoTotal"] = int(crecimiento)
        status["cdats"] = setCdats
        
        tasasCdats = CrecimientoCDAT.objects.all()
        comision = 0
        for tasas in tasasCdats:
            if tasaPromedio >= float(tasas.tasaMin) and tasaPromedio <= float(tasas.tasaMax):
                valorComision = tasas.comision
                
        comision = (crecimiento / 1000000) * (plazoPromedio / 360) * int(valorComision.replace(".", ""))
        status["comision"] = int(comision)
    if porcentaje < 80 and str(asesor.rol) != "Director Capt":
        status["state"] = False
        status["message"] = f"Este mes no cumplio con el 80% de su meta mensual individual en Captaciones (Suma de CDAT, Cooviahorro y Ahorro Vista)."
        status["porcentaje"] = f"Su porcentaje ejecutado fue: {porcentaje}"
    
    return status

