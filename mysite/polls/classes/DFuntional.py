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