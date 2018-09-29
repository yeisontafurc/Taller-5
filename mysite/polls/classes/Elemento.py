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