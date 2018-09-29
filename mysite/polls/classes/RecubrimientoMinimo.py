from .DFuntional import DFuncional
from .Util import Util
from copy import deepcopy

class RecubrimientoMinimo:
    #   Constructor
    def __init__(self, listaDF: []):
        self.listaDF = listaDF

    def set_lista_df(self, listaDF):
        if type(listaDF) is list:
            self.listaDF = listaDF;
        else:
            raise ValueError('listaDF debe ser una lista de dependencias funcionales')
    def get_lista_df(self):
        return self.listaDF

    def caclular_l1(self):
        Lorig = deepcopy(self.listaDF)
        L1 = self.eliminarElementales(self.descomponerDerecha(Lorig))
        return L1

    def eliminarElementales(self, ListaDf):
        try:
            i = len(ListaDf)
            while True:
                i = i - 1
                x = Util.StringToSortedString(ListaDf[i].getX())
                y = Util.StringToSortedString(ListaDf[i].getY())
                if x.find(y) != -1:  # preguntar si y esta contenido en x
                    ListaDf.pop(i)
                if (i == 0):
                    break
            return ListaDf
        except:
            raise ValueError('raise eliminarElementales')

    def descomponerDerecha(self, listaDep):
        tamano = len(listaDep)
        nuevaListaDF = []
        i = tamano
        while True:
            i = i - 1
            y = listaDep[i].getY()
            x = listaDep[i].getX()
            if len(y) > 1:
                for letter in y:
                    newDFun = DFuncional(x, letter)
                    nuevaListaDF.append(newDFun)
                listaDep.pop(i)
            if i == 0:
                break
        for depFun in nuevaListaDF:
            listaDep.append(depFun)
        return listaDep

    def calcular_l2(self):
        L = deepcopy(self.listaDF)
        cierresL1 = {}
        L2 = set()
        for x in L:
            eliminable = self.quitarAtributoExt(x, L, cierresL1)
            if type(eliminable) is DFuncional:
                L2.add(eliminable)
            else:
                L2.add(x)
        L2orig = deepcopy(L2)
        return L2orig

    @staticmethod
    def quitarAtributoExt(dfXIn, listaDepIn, cierres):
        dfX = deepcopy(dfXIn)
        listaDep = deepcopy(listaDepIn)
        flag = False
        if len(dfX.getX()) > 1:
            org = list(dfX.getX())
            y = dfX.getY()
            tamano = len(org)
            i = tamano
            while True:
                i = i - 1
                temp = deepcopy(org)
                temp.pop(i)
                nuevoX = "".join(str(x) for x in temp)
                dfCandidata = DFuncional(nuevoX, y)
                cierreX = Util.generarCierre(dfCandidata, listaDep)
                cierres[nuevoX] = cierreX
                if cierreX.find(y) != -1:
                    flag = True
                    temp = "".join(str(x) for x in temp)
                    break
                if (i == 0):
                    break
        if flag:
            return DFuncional(temp, dfX.getY())
        else:
            return None

    def calcular_l3(self, listaDF):
        listal3 = []
        for indice in listaDF:
            listal3.append(indice)
        L3 = self.eliminarDepRedundantes(listal3)
        return  L3

    def eliminarDepRedundantes(self,listaDF):
        i = len(listaDF)
        while True:
            i = i - 1
            dFCandidata = deepcopy(listaDF[i])
            listaDFaux = deepcopy(listaDF)
            listaDFaux.pop(i)
            cierreX = str(Util.generarCierre(dFCandidata, listaDFaux))
            try:
                if cierreX.find(dFCandidata.getY()) != -1:
                    listaDF.pop(i)
            except:
                raise ValueError("Error en eliminarDepRedundantes")
            if i == 0:
                break
        return listaDF

    def esEquivalente(self, recubrimientoMayor, recubrimientoMenor):
        #Recorrer recubrimientoMayor haciendo cierres sobre recubrimientoMenor
        for x in recubrimientoMayor:
            cierreX = Util.generarCierre(x, recubrimientoMenor)
            if (cierreX.find(x.getY()) == -1) :
                return False
        return True

    def compararContraRecubrimiento(self, recubrimientoInterno, recubrimientoExterno):
        # Verificar longitud de cada Recubrimiento mínimo
        equivalencia = False
        if(len(recubrimientoExterno) > len(recubrimientoInterno)):
            equivalencia = self.esEquivalente(recubrimientoExterno,recubrimientoInterno)
        else:
            equivalencia = self.esEquivalente(recubrimientoInterno,recubrimientoExterno)
        return equivalencia