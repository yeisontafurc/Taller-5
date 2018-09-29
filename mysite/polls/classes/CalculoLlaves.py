from copy import deepcopy
from .Util import Util
from .Elemento import elemento
from .DFuntional import DFuncional
from threading import Thread


class CalculoLlaves:
    def __init__(self, listaDF: [], alfabeto, m1, m2):
        self.listaDF = listaDF
        self.alfabeto = alfabeto
        self.m1 = m1
        self.m2 = m2

    def set_lista_df(self, listaDF):
        if type(listaDF) is list:
            self.listaDF = listaDF
        else:
            raise ValueError('listaDF debe ser una lista de dependencias funcionales')

    def set_alfabeto(self, alfabeto):
        self.alfabeto = alfabeto

    def set_m1(self, m1):
        self.m1 = m1

    def set_m2(self, m2):
        self.m2 = m2

    def get_m1(self):
        return self.m1

    def get_m2(self):
        return self.m2

    @staticmethod
    def hallarImplicados(listaDF):
        implicados = set([])
        for x in listaDF:
            ImpAux = elemento(x.getY())
            implicados.add(ImpAux)
        return implicados

    @staticmethod
    def hallarImplicantes(listaDF):
        implicantes = set([])
        for x in listaDF:
            if len(x.getX()) > 1:
                implicanteslargos = list(x.getX())
                for i in implicanteslargos:
                    ImpAux = elemento(i)
                    implicantes.add(ImpAux)
            else:
                ImpAux = elemento(x.getX())
                implicantes.add(ImpAux)
        return implicantes

    @staticmethod
    def calcularZ(alfabeto, listaImplicados):
        print("alfabeto: ",alfabeto)
        implic = list(listaImplicados)
        zetaCalculo = deepcopy(alfabeto)
        for alf in alfabeto:
            for imp in implic:
                if alf.find(str(imp)) != -1:
                    zetaCalculo.remove(alf)
        return zetaCalculo

    @staticmethod
    def unirWconZ(w, z):
        wsplit = list(w)
        for wi in wsplit:
            if z.find(wi) == -1:
                z = z + wi
        return z

    def llaveCandidata(self):
        # M1 Y M2
        self.m1 = set()
        self.m2 = set()
        alfabeto = self.alfabeto
        listaDF = self.listaDF
        listaDFAux = deepcopy(listaDF)
        # lista de llaves
        # Hallar y unir implicados (X->Y, X implicante Y implicado) agrupar en preZ, Z = alfabeto - preZ
        preZ = self.hallarImplicados(listaDFAux)
        print("Implicados: ", ''.join(str(x.getY()) for x in preZ) )
        z = self.calcularZ(alfabeto, preZ)
        porsiacas = self.calcularZ(alfabeto, preZ)
        # calcular cierre de Z
        # volver z una listaDF
        ZPreMas = ""
        for zi in z:
            ZPreMas = ZPreMas + zi
        zeta = deepcopy(ZPreMas)
        cierreZ = Util.generarCierre(DFuncional(ZPreMas, ""), listaDFAux)
        zetirijilla = self.calcularZ(alfabeto, cierreZ)
        if len(zetirijilla) == 0:
            elementoZ = elemento("".join(str(x) for x in sorted(porsiacas)))
            self.get_m2().add(elementoZ)
            return self.get_m2()
        else:
            listaDFAux = deepcopy(listaDF)
            # hallar y unir implicantes en preW, W = alfabeto - preW
            preW = self.hallarImplicantes(listaDFAux)
            w = self.calcularZ(alfabeto, preW)
            waux = ""
            for wi in w:
                waux = waux + wi
            wuz = self.unirWconZ(waux, cierreZ)
            v = self.calcularZ(alfabeto, wuz)
            listV = []
            for vaux in v:
                listV.append(vaux)
            listV = "".join(str(x) for x in sorted(listV))
            listV = list(listV)

            def worker(vi, conjunto_zeta, lista, M1, listaV):
                listaVSub = listaV
                if vi in listaV:
                    listaVSub = listaV[listaV.index(vi):]
                # print("LISTAV: ",str(listaV))
                if len(listaV) > 0:
                    # listaVSAVE = list(reversed(deepcopy(listaV)))
                    listaVSAVE = deepcopy(listaVSub)
                    vi = self.unirWconZ(vi, conjunto_zeta)
                    vi = "".join(str(x) for x in sorted(list(vi)))
                    # Calcular el cierre de vi
                    exists = False
                    for llave_en_m2 in self.m2:
                        if vi.find(llave_en_m2.getY()) != -1:
                            exists = True

                    cierreX = ""
                    if not exists:
                        cierreX = Util.generarCierre(DFuncional(vi, ""), lista)
                        print("cierre de ", vi, " es ", cierreX)
                        Util.imprimirListaDependencias(lista, " Cierre de " + vi + " es " + cierreX)
                    eme = elemento(vi)
                    M1.add(eme)
                    te = "".join(str(x) for x in sorted(alfabeto))
                    print(" VI es ", vi)
                    if cierreX == str(te):
                        self.get_m2().add(eme)
                        # print(" ",eme, " eS llave")

                    zeeeeta = listaVSAVE.pop(0)
                    vi = self.unirWconZ(vi, zeeeeta)
                    vi = "".join(str(x) for x in sorted(list(vi)))
                    print(" VI AFTERALL es ", vi)
                    worker(vi, conjunto_zeta, lista, deepcopy(M1), listaVSAVE)
                else:
                    return self.get_m2()

            threads = []
            listVi = deepcopy(listV)

            for ii in range(len(listV)):
                process = Thread(target=worker, args=[listV[ii], zeta, listaDFAux, self.get_m1(), deepcopy(listVi)])
                process.start()
                threads.append(process)
            for process in threads:
                process.join()

            for elementos in deepcopy(self.get_m2()):
                print("Llaves candidatas M2 : ", elementos)

            return None
