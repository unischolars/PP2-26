class x:#first parent
    def __init__(self,xval):
        self.x=xval
class y:#second parent
    def __init__(self,yval):
        self.y=yval
class coord (x,y):#child with multiple parents 
    def __init__(x_val,y_val):
        x.__init__(x_val)
        y.__init__(y_val)
    #if methods are the same python will go by mro and chose the most left parent 
