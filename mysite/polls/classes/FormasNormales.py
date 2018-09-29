from copy import deepcopy
from .CalculoLlaves import CalculoLlaves
from .DFuntional import DFuncional


class FormasNormales:
    def __init__(self, m2, listaDF, sfn_flag):
        self.m2 = m2
        self.listaDF = listaDF
        self.sfn_flag = sfn_flag

    def getM2(self):
        return self.m2

    def setM2(self, M2):
        self.m2 = M2

    def getListaDF(self):
        return self.listaDF

    def setListaDf(self, listaDF):
        self.listaDF = listaDF

    def getSfnFlag(self):
        return self.sfn_flag

    def setSfnFlag(self, sfn_flag):
        self.sfn_flag = sfn_flag

    def verificarSegundaFN(self):
        segundaFN = deepcopy(self.getListaDF())
        listaImplicados = CalculoLlaves.hallarImplicados(segundaFN)
        sfnBool = True
        M2 = deepcopy(self.getM2())
        self.setSfnFlag(True)
        for claveCandidata in M2:
            for impli in listaImplicados:
                if claveCandidata.getY().find(impli.getY()) == -1 or sfnBool is not True:
                    for sfn in segundaFN:
                        sfn = "".join(str(x) for x in sorted(list(sfn.getX())))
                        if sfn != claveCandidata.getY():
                            sfnBool = False
                            self.setSfnFlag(False)
                            break
                        if not sfnBool:
                            break
                    if not sfnBool:
                        break
                if not sfnBool:
                    break
            if not sfnBool:
                break
        return self.getSfnFlag()

    def verificarTerceraFN(self):
        if self.getSfnFlag():
            terceraFN = deepcopy(self.getListaDF())
            terceraBool = True
            for tfn in terceraFN:
                tfnjoined = "".join(str(x) for x in sorted(list(tfn.getX())))
                for claveCandidata in self.getM2():
                    if claveCandidata.getY().find(tfnjoined) == -1:
                        for impTFN in terceraFN:
                            if claveCandidata.find(impTFN.getY()) == -1:
                                terceraBool = False
                                return False
                                break
                            if not terceraBool:
                                break
                        if not terceraBool:
                            break
                    if not terceraBool:
                        break
                if not terceraBool:
                    break
            if terceraBool:
                return terceraBool

    def verificarFNBC(self):
        terceraFNBC = deepcopy(self.getListaDF())
        terceraBC = True
        for tfn in terceraFNBC:
            tfnjoined = "".join(str(x) for x in sorted(list(tfn.getX())))
            for claveCandidata in self.getM2():
                if claveCandidata.getY().find(tfnjoined) == -1:
                    terceraBC = False
                    return False
        if terceraBC:
            return True
