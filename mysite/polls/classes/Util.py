import json
#----- Clase de utilidades


class Util:
    @staticmethod
    def loadFile(path):
        with open(path) as f:
            data = json.load(f)
        return data

    @staticmethod
    def generarCombinaciones(dfX):
        listaDfX = list(dfX.x)
        print(listaDfX)

    @staticmethod
    def StringToSortedString(string):
        return "".join(str(x) for x in sorted(string))

    @staticmethod
    def generarCierre(dFuncionalX, listaDf):
        try:
            combinaciones = Util.getCombinaciones(dFuncionalX.getX())
        except:
            print("error generarCierre- combinaciones")
        bandera = True
        cierreX = ""
        i = 0
        while True:
            i = i + 1
            try:
                for combinacion in combinaciones:
                    cierreX = cierreX + Util.buscarCierreMas(combinacion, listaDf)
            except:
                print("Error al recorrer combinacion")

            cierreAux = sorted(set(cierreX))
            cierreX = "".join(str(x) for x in cierreAux)
            # print("cierreX: ",cierreX, " dFuncionalX.getX(): ",dFuncionalX.getX())
            if cierreX == dFuncionalX.getX():
                bandera = False

            dFuncionalX.setX(cierreX)

            try:
                combinaciones = Util.getCombinaciones(dFuncionalX.getX())
                #combinaciones = Util.getCombinaciones(cierreX)
            except:
                print("error al generar combinacion")

            if (bandera == False):
                # print("break")
                break

        return cierreX

    @staticmethod
    def potencia(c):
        """Calcula y devuelve el conjunto potencia del conjunto c. """
        if len(c) == 0:
            return [[]]
        r = Util.potencia(c[:-1])
        return r + [s + [c[-1]] for s in r]

    @staticmethod
    def contruirCombinacion(string):
        c = list(string)
        combinaciones = set([])
        for e in sorted(c, key=lambda s: (len(s), s)):
            comb = "".join(str(x) for x in sorted(e))  # convierte
            if comb != "":
                combinaciones.add(comb)
        return combinaciones

    @staticmethod
    def getCombinaciones(string):
        return Util.contruirCombinacion(Util.potencia(string))

    @staticmethod
    def buscarCierreMas(equis, listaDfL):

        equisEntrada = Util.StringToSortedString(equis)
        resultado = Util.StringToSortedString(equis)

        try:

            for dFLn in listaDfL:
                xOrden = Util.StringToSortedString(dFLn.getX())
                yOrden = Util.StringToSortedString(dFLn.getY())

                #if xOrden == equisEntrada:
                #    resultado = resultado + yOrden
                if equisEntrada.find(xOrden) != -1:
                    resultado = resultado + yOrden
        except:
            print("error al recorrer conjunto")

        return resultado

    #@staticmethod
    #def imprimirListaDependencias(listaDF, nombreLista: str):
    #    impresion = "</br>#############################################</br><b>" + nombreLista + "</b></br>#############################################</br>"
    #    return impresion + " ".join(str(x) for x in listaDF)
    def imprimirListaDependencias(listaDF, nombreLista: str):
        print("#################################")
        print("#     ",nombreLista,"     #")
        print("#################################")
        for x in listaDF:
            print (x)