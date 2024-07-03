from .read_excel import readExcel
from tasas.models import *
from users.models import *
import math

DAYS_29 = ["02", ]
DAYS_30 = ["04", "06", "09", "11"]
DAYS_31 = ["01", "03", "05", "07", "08", "10", "12"]
MONTHS = {
    '01': 'Enero',
    '02': 'Febrero',
    '03': 'Marzo',
    '04': 'Abril',
    '05': 'Mayo',
    '06': 'Junio',
    '07': 'Julio',
    '08': 'Agosto',
    '09': 'Septiembre',
    '10': 'Octubre',
    '11': 'Noviembre',
    '12': 'Diciembre'
}

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
            'V_TITULO': str(d['V_TITULO']).split(".")[0] if '.' in str(d['V_TITULO']) else "0",
            'M_ANTERIOR': str(d['M_ANTERIOR']).split(".")[0] if '.' in str(d['M_ANTERIOR']) else "0",
            'Q_PLADIA': str(d['Q_PLADIA']).split(".")[0] if '.' in str(d['Q_PLADIA']) else "0",
            'V_NUEVO': int(str(d['V_TITULO']).split(".")[0] if '.' in str(d['V_TITULO']) else "0") - int(str(d['M_ANTERIOR']).split(".")[0] if '.' in str(d['M_ANTERIOR']) else "0"),
            'FACTOR_PLAZO': round(d['Q_PLADIA'] / 360, 2),
            'T_NOMINAL': round(d['T_NOMINAL'], 3),
        }
        for d in setListCdats]
    
    totalNuevo = sum(int(value['V_NUEVO']) for value in setCdats)
    totalRenovado = sum(int(value['M_ANTERIOR']) for value in setCdats)
    
    valuesCdats = Cdat.objects.all()
    
    if "Capt" in str(asesor.rol):
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
                diferencia = round(abs(cdats['T_EFECTIVA'] - tasas.tasa), 2)
                if diferencia >= 0.5:
                    factorTasa = round(1 - (cdats['T_EFECTIVA'] - tasas.tasa), 3) + 0.5
                else:
                    if cdats["T_EFECTIVA"] > tasas.tasa:
                        factorTasa = round(1 - (cdats['T_EFECTIVA'] - tasas.tasa), 3) + diferencia 
                    else:
                        factorTasa = round(1 - (cdats['T_EFECTIVA'] - tasas.tasa), 3) 
                cdats['F_TASA'] = round(factorTasa, 3)
                if cdats['F_TASA'] > 2:
                    cdats['F_TASA'] = 2.0
                if cdats['F_TASA'] < 0:
                    cdats['F_TASA'] = 0
                if cdats['FACTOR_PLAZO'] > 2.0:
                    cdats['FACTOR_PLAZO'] = 2.0
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


def ahorroVista(name, current_file, month):
    """"""
    ahorrosVista = AhorroVista.objects.all()
    if str(month) in DAYS_29:
        days = 29
    elif str(month) in DAYS_30:
        days = 30
    elif str(month) in DAYS_31:
        days = 31
    else:
        days = 28
    ahorros = readExcel(name,
                        "Promedio AhorroVista",
                        "PROMOTOR",
                        ["CEDULA ASOCIADO", "CUENTA ASOCIADO", f"Promedio {days} días", "PROMOTOR"],
                        current_file)
    setAhorros = [
        {
            'CEDULA': d['CEDULA ASOCIADO'],
            'CUENTA': d['CUENTA ASOCIADO'],
            'PROMEDIO': int(d[f"Promedio {days} días"])
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


def crecimientoBase(name, current_file, month):
    """"""
    asesor = Asesor.objects.get(name=name)
    setname = name.split(" ")
    setList = []
    comision = 0
    for word in setname:
        setList.append(word.capitalize())
    newName = " ".join(setList)
    crecimientoBase = CrecimientoBaseSocial.objects.all()[0]
    nameMonth = MONTHS[month]
    crecimiento = readExcel(newName,
                            f"Afiliaciones Promotor {nameMonth}",
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


def checkMeta(name, fileCDAT, fileCoovi, fileAhorro, fileComisiones, date, fileAhorroVista):
    asesor = Asesor.objects.get(name=name)
    setname = name.split(" ")
    setList = []
    date = str(date).split("-")
    currentDate = f"{date[1]}-{date[0]}"
    nameMonth = MONTHS[date[0]]
    if str(date[0]) in DAYS_29:
        days = 29
    elif str(date[0]) in DAYS_30:
        days = 30
    elif str(date[0]) in DAYS_31:
        days = 31
    else:
        days = 28
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
                        f"CDAT Promotor {nameMonth}",
                        "Gestor",
                        ["Gestor", "EJEC", "PPTO", "% CUMP"],
                        fileCDAT
                        )
    cooviahorro = readExcel(newName,
                        f"Cooviahorro Promotor {nameMonth}",
                        "Gestor",
                        ["Gestor", "EJEC", "PPTO", "% CUMP"],
                        fileCoovi
                        )
    ahorroVista = readExcel(newName,
                        f"Ahorro Vista Promotor {nameMonth}",
                        "Gestor",
                        ["Gestor", "EJEC", "PPTO", "% CUMP"],
                        fileAhorro
                        )
    
    
    if len(cdat) == 0 or len(cooviahorro) == 0 or len(ahorroVista) == 0:
        porcentaje = 0
        if "Director" in str(asesor.rol):
            status["message"] = f"Este mes no cumplio con el 80% de su meta mensual individual en Captaciones (Suma de CDAT, Cooviahorro y Ahorro Vista)." 
    else:
        ejecutadosCdat = int(cdat[0]["EJEC"]) if cdat[0]["EJEC"] else 0
        ejecutadosCoovi = int(cooviahorro[0]["EJEC"]) if cooviahorro[0]["EJEC"] else 0
        ejecutadosAhorro = int(ahorroVista[0]["EJEC"]) if ahorroVista[0]["EJEC"] else 0
        ejecutados = ejecutadosCdat + ejecutadosCoovi + ejecutadosAhorro
        
        metaCdat = int(cdat[0]["PPTO"]) if cdat[0]["PPTO"] else 0
        metaCoovi = int(cooviahorro[0]["PPTO"]) if cooviahorro[0]["PPTO"] else 0
        metaAhorro = int(ahorroVista[0]["PPTO"]) if ahorroVista[0]["PPTO"] else 0
        meta = metaCdat + metaCoovi+ metaAhorro
        porcentaje = round((ejecutados / meta) * 100, 2)
    
    
    if status["director"] == True or porcentaje < 80 and str(asesor.rol) == "Director Capt":
        status["state"] = True
        status["stateCdat"] = True
        status["message"] = f"Felicitaciones este mes cumplio con su meta mensual individual."
        status["porcentaje"] = f"Su porcentaje ejecutado fue: {porcentaje}"

        # Crecimiento Ahorro Vista
        promedioAhorroVista = readExcel(str(asesor.sucursal),
                    "Promedio AhorroVista",
                    "SUCURSAL_PRODUCTO",
                    ["CEDULA ASOCIADO", "CUENTA ASOCIADO", f"Promedio {days} días", "PROMOTOR", "SUCURSAL_PRODUCTO", "Total"],
                    fileAhorroVista)

        # Crecimiento Cdats
        if str(asesor.rol) == "Director Capt":
            cdats = readExcel(name=str(asesor.subzona),
                    file="Cdat",
                    columns=["K_IDTERC", "NOMBRE_TERCERO", "V_TITULO", "F_TITULO", "Q_PLADIA", "M_ANTERIOR", "T_EFECTIVA", "T_NOMINAL", "RETENCION", "PROMOTOR", "SUBZONA", "SUC_PRODUCTO"],
                    archive=fileComisiones)
            cooviahorros = readExcel(name=str(asesor.sucursal),
                                    file="Cooviahorro",
                                    columns=["AANUMNIT", "K_NUMDOC", "N_TIPODR", "SALDO", "PROMOTOR", "SUC_PRODUCTO"],                    
                                    archive=fileComisiones)
            
            asesorsCapt = Asesor.objects.all()
            asesorsCapt = [asesors for asesors in asesorsCapt if "Capt" in str(asesors.rol)]
            
            setListCdats = [data for data in cdats if data.get('PROMOTOR') in [asesor.name for asesor in asesorsCapt]]
            setListCooviahorro = [data for data in cooviahorros if data.get('PROMOTOR') in [asesor.name for asesor in asesorsCapt]]
            setPromedioAhorroVista = [data for data in promedioAhorroVista if data.get('PROMOTOR') in [asesor.name for asesor in asesorsCapt]]
                                        
            setCdatsDate = [cdat for cdat in setListCdats if str(str(cdat['F_TITULO']).split(" ")[0])[:-3] == currentDate]
            
        else:
            cdats = readExcel(name=str(asesor.sucursal),
                file="Cdat",
                asesor="SUC_PRODUCTO",
                columns=["K_IDTERC", "NOMBRE_TERCERO", "V_TITULO", "F_TITULO", "Q_PLADIA", "M_ANTERIOR", "T_EFECTIVA", "T_NOMINAL", "RETENCION", "PROMOTOR", "SUBZONA", "SUC_PRODUCTO"],
                archive=fileComisiones)
            cooviahorros = readExcel(name=str(asesor.sucursal),
                    file="Cooviahorro",
                    asesor="SUC_PRODUCTO",
                    columns=["AANUMNIT", "K_NUMDOC", "N_TIPODR", "SALDO", "PROMOTOR", "SUC_PRODUCTO"],
                    archive=fileComisiones)
            
            setListCooviahorro = cooviahorros
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
            status["stateCdat"] = False
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
        
        # Crecimiento Cooviahorro  
        setCooviahorros = [
            {**d,
                'SALDO': str(d['SALDO']).split(".")[0] if '.' in str(d['SALDO']) else '0',
            }
            for d in setListCooviahorro]
        
        totalCoovi = sum(int(value['SALDO']) for value in setCooviahorros)
        if not CrecimientoCooviahorroMonth.objects.filter(name=asesor.sucursal, year=date[1], month=date[0]).exists():
            crecimientoCoovi = CrecimientoCooviahorroMonth(name=asesor.sucursal,
                                                value=int(totalCoovi),
                                                year=date[1],
                                                month=date[0])
            crecimientoCoovi.save()
        controlCooviahorros = CountCrecimientoCooviahorro.objects.all()[0].value
        listCrecimientoCoovi = CrecimientoCooviahorroMonth.objects.filter(name=asesor.sucursal)
        listCrecimientoCooviValues = [date.value for date in listCrecimientoCoovi]
        valueMaxCoovi = 0
        control = 0
        for cooviValue in listCrecimientoCooviValues:
            if control <= controlCooviahorros and control > 0:
                if cooviValue > valueMaxCoovi:
                    valueMaxCoovi = cooviValue
                control += 1
            if cooviValue == totalCoovi:
                control = 1

        crecimientoCoovi = totalCoovi - valueMaxCoovi
        if crecimientoCoovi < 0:
            crecimientoCoovi = 0
        
        
        comisionValueCoovi = CrecimientoCooviahorro.objects.all()[0].value.replace(".", "")
        comisicionCoovi = (int(crecimientoCoovi) / 1000000) * int(comisionValueCoovi)
        status["crecimientosCoovi"] = listCrecimientoCoovi
        status["crecimientoCoovi"] = crecimientoCoovi
        status["comisionCoovi"] = int(comisicionCoovi)
        
        #Ahorro Vista
        setPromedioAhorroVista = [
            {**d,
                'promedio': str(d[f'Promedio {days} días']).split(".")[0] if '.' in str(d[f'Promedio {days} días']) else '0',
                'total': str(d['Total']).split(".")[0] if '.' in str(d['Total']) else '0',
            }
            for d in promedioAhorroVista]
        # print(len(setPromedioAhorroVista))
        # setPromedioAhorroVista = [d for d in setPromedioAhorroVista if d['PROMOTOR'] != "DEFAULT"]
        # print(len(setPromedioAhorroVista))
        promedio = sum(int(value['promedio']) for value in setPromedioAhorroVista)
        # print(promedio)
        
    if porcentaje < 80 and str(asesor.rol) != "Director Capt":
        status["state"] = False
        status["message"] = f"Este mes no cumplio con el 80% de su meta mensual individual en Captaciones (Suma de CDAT, Cooviahorro y Ahorro Vista)."
        status["porcentaje"] = f"Su porcentaje ejecutado fue: {porcentaje}"
    
    return status

