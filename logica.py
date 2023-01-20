from datetime import datetime
from conexion import Conexion

'''
tarifa = [
    (0,100,0.33),
    (101,150,1.07),
    (151,200,1.43),
    (201,250,2.46),
    (251,300,3.0),
    (301,350,4.0),
    (351,400,5.0),
    (401,450,6.0),
    (451,500,7.0),
    (501,600,9.2),
    (601,700,9.45),
    (701,1000,9.85),
    (1001,1800,10.8),
    (1801,2600,11.8),
    (2601,3400,12.9),
    (3401,4200,13.95),
    (4201,5000,15.0),
    (5001,'final',20.0)
] # más de 5000 a 20.00
'''
rangos = []


def getTarifaBD(t):

    global rangos

    try:
        cn = Conexion()
        q = cn.cursor.execute("SELECT rangos FROM tarifas WHERE tarifa = '%s'" % (t))
        rows = q.fetchone()
        cn.desconectar()
    except:
        print('Error al intentar acceder a la BD.')
        return

    rangos_str = list(map(lambda x: x.split('-'),rows[0].split(',')))
    rangos = list(map(lambda x: (int(x[0]),int(x[1]),float(x[2])),rangos_str[:-1]))
    rangos.append((int(rangos_str[-1][0]),rangos_str[-1][1],float(rangos_str[-1][2])))
    

def getCalculo(info=None,tarifa=None,solo_cadena=False,solo_tpl=False,consumo=None,estimado=False):

    if consumo is None:
        consumo = int(info[1]) - int(info[0])
    else:
        consumo = consumo
    if tarifa is None and not estimado:
        tarifa = info[6]
    importe_total = 0.0
    result_str = 'CONSUMO:\n\n'

    def getPronostico(): # dias,consumo_diario,consumo

        if dias == 30 or dias > 30 or dias < 0:
            return None,None
        dias_prox = 30 - dias
        consumo_estimado = round((consumo_diario*dias_prox)+consumo)
        importe_estimado =getCalculo(consumo=consumo_estimado,estimado=True)
        return consumo_estimado,round(importe_estimado,2)

    def make_str(r,last=False):

        kw = 0
        if last:
            if r[0] != 0:
                kw = consumo - (r[0]-1)
            else:
                kw = consumo - r[0]
        else:
            if r[0] != 0:
                kw = r[1] - (r[0]-1)
            else:
                kw = r[1] - r[0]
        importe_rango = kw * r[2]
        nonlocal importe_total
        nonlocal result_str
        importe_total += importe_rango
        result_str += f'Rango {r[0]}-{r[1]}, {kw}kws x {r[2]} = {round(importe_rango,2)}\n'
        if last:
            result_str += f'\nPara un CONSUMO TOTAL de {consumo}kws, a pagar {round(importe_total,2)}'

    def getConsumoDiario():
        
        if info[2] != 'fecha' and info[2] != '' and info[2] != None and info[3] != 'fecha' and info[3] != '' and info[3] != None:
            anterior = datetime.strptime(info[2],'%d/%m/%Y').date()
            actual = datetime.strptime(info[3],'%d/%m/%Y').date()
            if anterior == actual:
                dias = 1
            else:
                dias = (actual-anterior).days
        else:
            dias = 30

        consumo_diario = consumo / dias
        return consumo_diario,dias
    

    if not estimado:
        getTarifaBD(tarifa)
        #for i in tarifa: print(i)

    for rango in rangos:

        if rangos.index(rango) == len(rangos) - 1:
            make_str(rango,last=True)
            break
        else:
            if consumo in range(rango[0],rango[1]+1):
                make_str(rango,last=True)
                break
            else:
                make_str(rango)

    if not estimado and not solo_cadena:
        consumo_diario, dias = getConsumoDiario()
        consumo_estimado,importe_estimado = getPronostico() # dias,consumo_diario,consumo
        result_tpl = (round(consumo_diario),consumo,round(importe_total,2),dias,consumo_estimado,importe_estimado)

    if estimado:
        return importe_total

    if solo_cadena:
        return result_str

    if solo_tpl:
        return result_tpl

    return result_tpl, result_str