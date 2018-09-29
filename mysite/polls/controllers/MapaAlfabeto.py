import string

class MapaAlfabeto:
    def __init__(self, alfabeto, llaveValor :[]):
        self.alfabeto = sorted(alfabeto)
        self.llaveValor = llaveValor

    def setAlfabeto(self, alfabeto):
        self.alfabeto = alfabeto

    def getAlfabeto(self):
        return self.alfabeto

    def crearMapa(self):
        class KeyValue:
            def __init__(self, key, value):
                self.key = key
                self.value = value
        i = 0
        lista_soportada = string.printable
        self.llaveValor = []
        for word in self.getAlfabeto():
            self.llaveValor.append(KeyValue(lista_soportada[i], word))
            i = i + 1
        return self.llaveValor

    def obtenerChar(self,string):
        for ii in self.llaveValor:
            if(ii.value == string):
                return ii.key

    def obtenerStringFromChar(self, string):
        for ii in self.llaveValor:
            if(ii.key == string):
                return ii.value