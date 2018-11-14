from rockets import Component



class commandmodule(Component):


    def __init__(self, body, vertices, transform=None, radius=0):
        Component.__init__(self, body, vertices, transform, radius)
        
    #this should control the rocket

