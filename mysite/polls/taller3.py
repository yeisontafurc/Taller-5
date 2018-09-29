from copy import deepcopy
import json
from collections import namedtuple
from threading import Thread
import matplotlib.pyplot as plt
import numpy as np

from IPython.display import display,clear_output 
from ipywidgets import Output, widgets





#----- Clase de utilidades
class Util:
        def loadFile(self, path):
            with open(path) as f:
                data = json.load(f)
            return data
        def generarCierre(self,dfX, listaDf):
            dfX=listaDf
        def generarCombinaciones(self,dfX):
            listaDfX = list(dfX.x)
            print(listaDfX)

            
#---- Clase DFuncional: Dependencia funcional con los atributos X:str (implicante) y Y:str (Implicado)
class DFuncional:
#------ constructor
    def __init__(self, x: str, y:str):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self,x):
        self.x = x
    def setY(self,y):
        self.y = y
    #def __str__(self):
    #    return '{{"x" = "{0}","y" = "{1}"}}'.format(self.x, self.y)
    def __str__(self):
        return '{{"{0}"->"{1}"}}'.format(self.x, self.y)
    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y )
    def __hash__(self):
        return hash((self.x,self.y))

class elemento:
    def __init__(self, y:str):
        self.y = y
    def getY(self):
        return self.y
    def setY(self,y):
        self.y = y
    #def __str__(self):
    #    return '{{"x" = "{0}","y" = "{1}"}}'.format(self.x, self.y)
    def __str__(self):
        return '{0}'.format(self.y)
    def __eq__(self, other):
        return (self.y == other.y)
    def __hash__(self):
        return hash((self.y))

#---- Clase Relacion
#---- TODO 
class Relacion:
    def __init__(self, t, df):
        self.df = df
        self.t = t
#--------------------------------------------


primera = 0
listaX = set([])
listaY = set([])
def combinar(conjunto: set):
    print("*****combinar******")

    try:
        global primera
        if  primera == 0:
            listaX.add( conjunto.pop())

            primera = 1
        else:
            listaY.add("".join(str(x) for x in conjunto.pop()))

        listaY.add("".join(str(x) for x in conjunto))

        if len(conjunto)>1:
            combinar(conjunto)
    except:
        print("Error en combinar")
        
    
                
def getCombinaciones2(string: str):
    print("*******getCombinaciones****** ", string)
    combinacion = set([])
    lista = set(string)
    try:
        combinar(lista)
    except:
        print("error combinar")

    try:
        for indicex in listaX:
            combinacion.add(indicex)
    except:
        print("Error al recorrer ListaX")
    try:

        for indicey in listaY:
            combinacion.add(indicey)
    except:
        print("Error al recorrer ListaX")

    try:
        for indicex in listaX:
            print("indicex: ---", indicex )
            for indicey in listaY:
                setAux = set(indicex+indicey)
                string = "".join(str(x) for x in sorted(setAux))
                combinacion.add(string)
                print("indicey: ---", indicey )

    except:
        print("Error al recorrer listaX")
        
    return combinacion

#getCombinaciones("ABCDF")



#--- Generación del cierre de X respecto a L
def generarCierre(dFuncionalX, listaDf):
    #print("Generar cierre de: " , dFuncionalX.getX())

    try:
        combinaciones = getCombinaciones(dFuncionalX.getX())
    except:
        print("error generarCierre- combinaciones")
    bandera = True
    cierreX = ""
    while True:
        try:
            for combinacion in combinaciones:
                cierreX = cierreX + buscarCierreMas(combinacion, listaDf)
        except:
            print("Error al recorrer combinacion")
      
        cierreAux = sorted(set(cierreX))
        cierreX = "".join(str(x) for x in cierreAux)
        #print("cierreX: ",cierreX, " dFuncionalX.getX(): ",dFuncionalX.getX())
        if cierreX == dFuncionalX.getX():
            bandera = False
        
        dFuncionalX.setX(cierreX)

        try:
            combinaciones = getCombinaciones(dFuncionalX.getX());
        except:
            print("error al generar combinacion")
            
        if(bandera == False):
            #print("break")
            break
            
    return cierreX

def generarCierreAsync(dFuncionalX, listaDf):
    #print("Generar cierre de: " , dFuncionalX.getX())

    try:
        combinaciones = getCombinaciones(dFuncionalX.getX())
    except:
        print("error generarCierre- combinaciones")
    bandera = True
    cierreX = ""
    while True:
        try:
            for combinacion in combinaciones:
                cierreX = cierreX + buscarCierreMas(combinacion, listaDf)
        except:
            print("Error al recorrer combinacion")
      
        cierreAux = sorted(set(cierreX))
        cierreX = "".join(str(x) for x in cierreAux)
        #print("cierreX: ",cierreX, " dFuncionalX.getX(): ",dFuncionalX.getX())
        if cierreX == dFuncionalX.getX():
            bandera = False
        
        dFuncionalX.setX(cierreX)

        try:
            combinaciones = getCombinaciones(dFuncionalX.getX());
        except:
            print("error al generar combinacion")
            
        if(bandera == False):
            #print("break")
            break
    return cierreX



def buscarCierreMas(equis, listaDfL):
    #print(equis,"+")

    equisEntrada = "".join(str(x) for x in sorted(equis)) 
    resultado = "".join(str(x) for x in sorted(equis)) 

    #print("Recorriendo lista de dependencias")
    try:

        for dFLn in listaDfL:
            xOrden = "".join(str(x) for x in sorted(dFLn.getX()))
            yOrden = "".join(str(x) for x in sorted(dFLn.getY()))
            #print("deendenciaN", dFLn, "")
            
            if xOrden == equisEntrada:
                resultado =  resultado + yOrden
    except:
        print("error al recorrer conjunto")
    #print("*Cierre de", equis," =",resultado)

    return resultado



def ordenarElementosXY(ListaDf):
    print("*****ordenarElementosXY******")

    try:
        print("ListaDf", ListaDf)

        listaOrdenada = []
        tamano = len(ListaDf)

        i = tamano
        while True:
            i = i-1

            x =  "".join(str(x) for x in sorted(ListaDf[i].getX())) # convierte 
            y =  "".join(str(x) for x in sorted(ListaDf[i].getY())) # convierte

            nuevaDf = DFuncional(x,y) 

            
            listaOrdenada.append(nuevaDf)

            if(i==0):
                break
        return listaOrdenada
    except:
        print("error ordenarElementos")

     

            
def eliminarElementales(ListaDf):
    print("Método eliminar duplicados")

    try:
        print("ListaDf", "".join(str(x) for x in list(ListaDf)))

        tamano = len(ListaDf)

        i = tamano
        while True:
            i = i-1

            x =  "".join(str(x) for x in sorted(ListaDf[i].getX())) # convierte 
            y =  "".join(str(x) for x in sorted(ListaDf[i].getY())) # convierte
            if x.find(y) != -1 :                                        # preguntar si y esta contenido en x
                ListaDf.pop(i)

            if(i==0):
                break
        return ListaDf
    except:
        print("error eliminarElementales")

        
        

def descomponerDerecha(listaDep):
    print("Método Descomponer implicado")

    tamano = len(listaDep)

    nuevaListaDF = []
    i = tamano
    while True:
        i = i-1

        y = listaDep[i].getY()
        x = listaDep[i].getX()
        
        
        
        if len(y) > 1:
            
            for letter in y:
                newDFun = DFuncional(x,letter)
                nuevaListaDF.append(newDFun)
            
            listaDep.pop(i)   

        
        if(i==0):
            break
            
    for depFun in nuevaListaDF:
        listaDep.append(depFun)
       
    return listaDep

def quitarAtributoExt(dfX ,listaDep, cierres):
    print("Método: quitarAtributoExtraño")

    flag = False
    if len(dfX.getX())>1:
        print("Posible dependencia extraña",dfX)
        #-ABC->D implicante: ABC implicado D
        #-Separar implicante ABC => A,B,C
        org = list(dfX.getX())
        y = dfX.getY()
        tamano = len(org)
        i = tamano
        while True:
            i = i-1
            temp = deepcopy(org)
            temp.pop(i)
            nuevoX =  "".join(str(x) for x in temp)            
            dfCandidata = DFuncional(nuevoX, y)
            cierreX = generarCierre(dfCandidata, listaDep)
            cierres[nuevoX]=cierreX
            if cierreX.find(y) != -1:
                print("encontrada.... " , dfCandidata)
                flag = True
                temp = "".join(str(x) for x in temp)
                break
            if(i==0):
                break
        
    if flag:
        return  DFuncional(temp,dfX.getY())
    else:
        return None
    
       
def potencia(c):
    """Calcula y devuelve el conjunto potencia del conjunto c. """
    if len(c) == 0:
        return [[]]
    r = potencia(c[:-1])
    return r + [s + [c[-1]] for s in r]



def contruirCombinacion(string):
    c=list(string)
    combinaciones = set([])
    for e in sorted(c, key=lambda s: (len(s), s)):
        comb= "".join(str(x) for x in sorted(e)) # convierte
        if comb != "":
            combinaciones.add(comb)
    return combinaciones      
        
def getCombinaciones(string):
    #print("Método generar combinaciones de: "+string)
    return contruirCombinacion( potencia(string))
    
        
def imprimirListaDependencias(listaDF, nombreLista :str):
    print("#################################")
    print("#     ",nombreLista,"     #")
    print("#################################")
    for x in listaDF:
        print (x)
    return None





def eliminarDepRedundantes(listaDF):
    print("*****************************************************************")

    i = len(listaDF)

    while True:
        i = i-1
        print("---------- i: " , i )
        print("---------- listaDF[i] : " , listaDF[i]  )

        dFCandidata = deepcopy(listaDF[i] )
        listaDFaux  = deepcopy(listaDF)
        listaDFaux.pop(i)

        cierreX = str(generarCierre(dFCandidata, listaDFaux))

        print( "Cierreeeeeeeeeeeeeeeeeeeeeeeeee",cierreX , dFCandidata.getY())
        try:
            print("dFCandidata.getY() - ", dFCandidata.getY())
            if cierreX.find(dFCandidata.getY()) != -1:
                print("Eliminada----")
                listaDF.pop(i)
        except:
            print("error en cierre")
        if(i==0):
            break
    return listaDF

##
## TALLER 2
##
def hallarImplicados(listaDF):
    implicados = set([])
    for x in listaDF:
        ImpAux = elemento(x.getY())
        implicados.add(ImpAux)
    return implicados

def hallarImplicantes(listaDF):
    implicantes = set([])
    for x in listaDF:
        if len( x.getX() ) > 1 :
            implicanteslargos = list(x.getX())
            for i in implicanteslargos:
                ImpAux = elemento(i)
                implicantes.add(ImpAux)
        else:
            ImpAux = elemento(x.getX())
            implicantes.add(ImpAux)
    return implicantes

def calcularZ(alfabeto, listaImplicados):
    implic = list(listaImplicados)
    zetaCalculo = set()
    zetaCalculo = deepcopy(alfabeto)
    for alf in alfabeto:
        for imp in implic:
            if(alf.find(str(imp)) != -1):
                zetaCalculo.remove(alf)
    return zetaCalculo

def unirWconZ(w,z):
    wsplit = list(w)
    for wi in wsplit:
           if(z.find(wi) == -1):
               z = z + wi
    return z


    return

#def addListaM1(implicante, cierre,universo):    
#    M1=set()
#    if cierre!= universo:
        
        

def llaveCandidata(alfabeto,listaDF):
    #M1 Y M2
    M1=set()
    M2=set()
    
    
    listaDFAux = deepcopy(listaDF)
    #lista de llaves
    #Hallar y unir implicados (X->Y, X implicante Y implicado) agrupar en preZ, Z = alfabeto - preZ
    preZ = hallarImplicados(listaDFAux)
    
    z = calcularZ(alfabeto,preZ)
    porsiacas = calcularZ(alfabeto,preZ)
    #calcular cierre de Z
    #volver z una listaDF
    ZPreMas = ""
    for zi in z:
        ZPreMas = ZPreMas + zi
    zeta = deepcopy(ZPreMas)
    cierreZ = generarCierre(DFuncional(ZPreMas,""),listaDFAux)
    zetirijilla = calcularZ(alfabeto,cierreZ)
    if len(zetirijilla) == 0:
        print(" Z es llave única, z es ", porsiacas)
        M2.add("".join(str(x) for x in sorted((porsiacas))))
        return M2
    else:
        listaDFAux = deepcopy(listaDF)
        # hallar y unir implicantes en preW, W = alfabeto - preW
        preW = hallarImplicantes(listaDFAux)
        imprimirListaDependencias(preW,"Implicantes")
        w = calcularZ(alfabeto, preW)
        imprimirListaDependencias(w,"Grupo W")
        
        waux = ""
        for wi in w:
            waux = waux + wi
        wuz = unirWconZ(waux,cierreZ)
        imprimirListaDependencias(list(wuz),"Grupo WZ ")
        v = calcularZ(alfabeto, wuz)
        #imprimirListaDependencias(v,"Grupo V de vendetta")
        
        listV = []
        for vaux in v:
            listV.append(vaux)
        #threads = list()
        #for vi in listV:
        #    t = threading.Thread(target=worker(vi,zeta,listaDFAux,M1))
        #    threads.append(t)
        #    t.start()
        
        listV = "".join(str(x) for x in sorted((listV)))
        listV = list(listV)
        print(listV)
        #print("ZETA antes de worker: ",zeta)
        def worker(vi, zeta, lista, M1, listaV):
            listaVSub = listaV;
            if vi in listaV:
                listaVSub = listaV[listaV.index(vi):]
            #print("LISTAV: ",str(listaV))
            if(len(listaV) > 0):
                #listaVSAVE = list(reversed(deepcopy(listaV)))
                listaVSAVE = deepcopy(listaVSub)
                vi = unirWconZ(vi,zeta)
                vi = "".join(str(x) for x in sorted(list(vi)))
                #print(" LALALA ANTES:", vi)
                #Calcular el cierre de vi
                exists = False
                for elementos in M2:
                    if(vi.find(elementos.getY()) != -1):
                        exists = True
                        
                cierreX = ""
                if exists == False:
                    cierreX =  generarCierre(DFuncional(vi,""),lista)
                    print("cierre de ",vi, " es ",cierreX)
                eme = elemento(vi)
                M1.add(eme)
                te = "".join(str(x) for x in sorted(alfabeto))
                print(" VI es ",vi)
                if cierreX == str(te):
                    M2.add(eme) 
                    #print(" ",eme, " eS llave")
               
               
                zeeeeta = listaVSAVE.pop(0)
                vi = unirWconZ(vi,zeeeeta)
                vi = "".join(str(x) for x in sorted(list(vi)))
                print(" VI AFTERALL es ",vi)
                worker(vi, zeta, lista, deepcopy(M1), listaVSAVE)
            else:
                return M2
           
        ###FIN WORKER    
         
            
            #worker((zuvi+listAux), zeta, lista, M1, listAux)
            
        threads = []
        listVi = deepcopy(listV)
        
        for ii in range(len(listV)):
            process = Thread(target = worker, args=[listV[ii], zeta, listaDFAux, M1, deepcopy(listVi)])
            process.start()
            threads.append(process)
        for process in threads:
            process.join()
        
        
        #for cierre in M1:
        #    print(cierre)
        listallaves = deepcopy(M2)
        for elementos in deepcopy(M2):
            print("Llaves candidatas M2 : ", elementos)
        
        #for hilo in threads:
        #    print(hilo.is_alive)
        # unir Z+ y W en preV
        # V = T - preV
        # por cada elemento de V => V(i)
        # abrir tantos hilos como elementos de v
        # por cada hilo{ recursivamente unir z y v(i), y calcular cierre, si el cierre = T, se agrega la llave }
        return None




#########################################################
#
#                     INIT                              #
#
#########################################################
# Llamada a utilidades
#util = Util()
# Leer archivo JSON
#readJson = util.loadFile("relacion.json")
# convierte json en string
#entradaStr = json.dumps(readJson) 
#trasforma json a objeto
#y = json.loads(entradaStr, object_hook=lambda d: namedtuple('r', d.keys())(*d.values()))
#
#dependencias = []
#L = []
#dependencias = y.relacion.dFuncionales
#
#for x in dependencias:
#    depAux = DFuncional(x.x,x.y)
#    print(depAux)
#    L.append(depAux)
#
#recubrimiento = []
R2 = []
#recubrimiento = y.recubrimiento.dFuncionales
#for x in recubrimiento:
 #   depAux = DFuncional(x.x,x.y)
 #   R2.append(depAux)


    
# TALLER 2








def clickAgregar(agregarBt):
    #clear_output()
    x = InputX.value.upper()
    y = InputY.value.upper()

    if x == "":
        if mostrar == True:
            print("ingrese el valor X")        
    if y =="":
        if mostrar == True:
            print("ingrese el valor Y")


    if x != "" and y !="":
        
        nuevaDF = DFuncional(x,y)
        listaDUI.append(nuevaDF)
        InputX.value =""
        InputY.value =""
        
    if mostrar == True:
        print("L= ")
        
    for DFn in listaDUI:
        print(DFn)
#    listaDF
    with out:
        clear_output(wait=True)



def clickBorrar(borrarBt):

    listaDUI.clear()
    if mostrar == True:
        print("L= ")
    
    for DFn in listaDUI:
        print(DFn)
    with out:
        clear_output(wait=True)

        
def clickCalcular(calcularBt):
    t = InputT.value.upper()
    banderilla = True

    if len(listaDUI) < 1 and mostrar == True:
        print("Ingrese los atributos")
        banderilla = False

    if t == ""  and mostrar == True:
        print("Ingrese la lista de dependencias funcionales")
        banderilla = False
    
    if banderilla is True:
        
        
        
        cierresL1={}
        L = listaDUI
        Lorig = deepcopy(listaDUI)
        L1=eliminarElementales(descomponerDerecha(Lorig))
        L1orig = deepcopy(L1)
        L2= set()
        
        
        for x in L1:
            print("L1: Dependencia: ",x)
            eliminable = quitarAtributoExt(x, L,cierresL1)
            if type(eliminable) is DFuncional:
                print("X: ",x.getX(), "Y: ", x.getY(), " eliminable: ",eliminable)
                L2.add(eliminable)
            else:
                L2.add(x)
        
        
        L2orig = deepcopy(L2)
        listal3 = []
        
        for indice in L2:
            print("indice.... ",indice)
            listal3.append(indice)
        
        
        L3 = eliminarDepRedundantes(listal3)
        L3orig = deepcopy(L3)
        imprimirListaDependencias(L, "Conjunto dependencias L")
        imprimirListaDependencias(L1orig, "Conjunto dependencias L1")
        imprimirListaDependencias(L2orig, "Conjunto dependencias L2")
        imprimirListaDependencias(L3orig,"Conjunto dependencias L3")
        imprimirListaDependencias(R2,"Conjunto dependencias R2")
        
        alfa = t.split(",")
        M2 = llaveCandidata(set(alfa), L3orig)
        
        segundaFN = deepcopy(listaDUI)
        listaImplicados = hallarImplicados(segundaFN)
        sfnBool = True
        for claveCandidata in M2:
            for impli in listaImplicados:
                if( claveCandidata.find(impli.getY()) == -1 or sfnBool is not True):
                    for sfn in segundaFN:
                        sfn = "".join(str(x) for x in sorted(list(sfn.getX()))) 
                        if sfn != claveCandidata:
                            sfnBool = False
                            print("")
                            imprimirListaDependencias(segundaFN, " NO está en 2FN ni en 3FN ")
                            break
                        if not( sfnBool ):
                            break
                    if not( sfnBool ):
                        break
                if not( sfnBool ):
                    break
            if not( sfnBool ):
                break
        
        if (sfnBool):
            imprimirListaDependencias(segundaFN, " Está en 2FN ")
            terceraFN = deepcopy(listaDUI)
            alfabetoOrdenado = "".join(str(x) for x in sorted(alfa))
            terceraBool = True
            for tfn in terceraFN:
                tfnjoined = "".join(str(x) for x in sorted(list(tfn.getX())))                
                for claveCandidata in M2:
                    if( claveCandidata.find(tfnjoined) == -1):        
                        for impTFN in terceraFN:
                            if(claveCandidata.find(impTFN.getY()) == -1):
                                terceraBool = False
                                imprimirListaDependencias(terceraFN, " NO está en 3FN ")
                                break
                            if not (terceraBool):
                                break
                        if not (terceraBool):
                            break
                    if not (terceraBool):
                        break
                if not (terceraBool):
                    break
            if (terceraBool):
                imprimirListaDependencias(terceraFN, " Está en 3FN ")
            
            
            
            terceraFNBC = deepcopy(listaDUI)
            alfabetoOrdenado = "".join(str(x) for x in sorted(alfa))
            terceraBool = True
            for tfn in terceraFNBC:
                tfnjoined = "".join(str(x) for x in sorted(list(tfn.getX())))                
                for claveCandidata in M2:
                    if( claveCandidata.find(tfnjoined) == -1):        
                        terceraBool = False
                        imprimirListaDependencias(terceraFN, " NO está en FNBC ")
                          
            if (terceraBool):
                imprimirListaDependencias(terceraFN, " Está en FNBC ")                
                
        
        ###A PARIR PIÑAS CON 3FNBC
        
                            
            
        
        
        
            
            
        
    with out:
        clear_output(wait=True)
        
def clickSegundaFN(calcularSegundaFN):

    print("segunda forma normal")
    
    listaDUI.clear()
    if mostrar == True:
        print("L= ")
    
    for DFn in listaDUI:
        print(DFn)
    with out:
        clear_output(wait=True)

        
        
def clickTerceraFN(calcularTerceraFN):

    listaDUI.clear()
    if mostrar == True:
        print("L= ")
    
    for DFn in listaDUI:
        print(DFn)
    with out:
        clear_output(wait=True)
        
def clickBCFN(calcularFNBC):

    listaDUI.clear()
    if mostrar == True:
        print("L= ")
    
    for DFn in listaDUI:
        print(DFn)
    with out:
        clear_output(wait=True)
        

#-------------------------------------------------------------------------------
def mostrarPanel():

    

    titulo = widgets.Label("CALCULO DE LLAVES CANDIDATAS")

    clear_output(wait=True)

    display(titulo)

    left_box = widgets.VBox([InputX, InputY])

    right_box = widgets.VBox([agregarBt, borrarBt,botonCalcular])
    widgets.HBox([left_box, right_box])



out= Output()
agregarBt=widgets.Button(description='Agregar')
borrarBt=widgets.Button(description='Borrar')
calcularBt = widgets.Button(description='Recubrimiento minimo')

calcularSegundaFN = widgets.Button(description='2da FN')
calcularTerceraFN = widgets.Button(description='3ra FN')
calcularFNBC = widgets.Button(description='FNBC')




#display(widgets.HBox((agregarBt, borrarBt)))
out = Output()

InputT = widgets.Text(description="Atributos (T)", continuous_update=True)
InputX = widgets.Text(description="Implicante X", continuous_update=True)
InputY = widgets.Text(description="Implicado  Y", continuous_update=True)


listaDUI = list()

mostrar = False



agregarBt.on_click(clickAgregar)
clickAgregar("None")


borrarBt.on_click(clickBorrar)
clickBorrar("None")

calcularBt.on_click(clickCalcular)
#clickCalcular("None")

mostrar = True

titulo = widgets.Label("CALCULO DE LLAVES CANDIDATAS")


left_box = widgets.VBox([InputX, InputT ])
right_box = widgets.VBox([  InputY])

four_col =  widgets.VBox([  agregarBt, calcularBt, calcularSegundaFN, calcularTerceraFN,  calcularFNBC]) 

widgets.HBox([left_box, right_box, four_col ,borrarBt ])