#Michael Sporkin
#Global variables collective library
import numpy as np

class GlbVars:
    def __init__(self):
        self.link = False
        self.searching = True
        self.targetFound = False
        self.sweeping = True
        self.esc = False
        self.statBlue = False
        self.mobBlue = False
        
        self.actionString = ''
        self.actionString_update = 'Starting...'
        self.box = []
        self.center = []
        self.offsetAngles = np.array([0,0,0])
        self.centerFrame = (640,512) #center of frame
        
    def setTargetFound(self, boolVal):
        self.targetFound = boolVal
        
    def setSweeping(self, boolVal):
        self.sweeping = boolVal
        
    def setEsc(self, boolVal):
        self.esc = boolVal
    
    def setStatBlue(self, boolVal):
        self.statBlue = boolVal
    
    def setMobBlue(self, boolVal):
        self.mobBlue = boolVal
    
    def setLink(self, boolVal):
        self.link = boolVal
    
    def setAS(self, string):
        self.actionString = string
    
    def setASU(self, string):
        self.actionString_update = string
        
    def setBox(self, topLeft, topRight, bottomRight, bottomLeft):
        halfHeight = (topRight[1] - bottomRight[1])/2
        
        topLeft = (topLeft[0], topLeft[1]+halfHeight+halfHeight/5)
        topRight = (topRight[0], topRight[1]+halfHeight+halfHeight/5)
        bottomLeft = (bottomLeft[0], bottomLeft[1]+2*halfHeight+halfHeight/5)
        bottomRight = (bottomRight[0], bottomRight[1]+2*halfHeight+halfHeight/5)
        
        self.box = ( topLeft, topRight, bottomRight, bottomLeft )
        
    def setCenter(self, cx, cy):
        self.center = (cx, cy)
        
    def setOffsetAngles(self, oa):
        self.offsetAngles = oa
        
#global shutdown function
def escape(glbl):
    while glbl.esc == False:
        if input() == 'esc': #any input when not naming file will turn searching false
            glbl.setEsc(True)
    print('Shutting down...')
    #Shuts it down
    return