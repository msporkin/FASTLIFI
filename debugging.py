from GVars import *
from CameraLibrary import *

glbl = GlbVars()

def feedbackMobMod(glbl):
    blueLb = np.array([110, 150, 150])
    blueUb = np.array([130, 255, 255])
    
    while(True):
        _, frame1 = cap.read()
        blueHsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        blueMaskFramed = np.zeros(frame1.shape, np.uint8) # makes initial array of zeros in size of array
        
        #Mask out everything in the image except for one half the pixel height of the hexagon above the target
        blueMaskFramed[ int(glbl.box[0][1]):int(glbl.box[3][1]), int(glbl.box[0][0]):int(glbl.box[1][0]), :
                   ] = frame1[ int(glbl.box[0][1]):int(glbl.box[3][1]), int(glbl.box[0][0]):int(glbl.box[1][0]), : ]
        blueMask = cv2.inRange(blueHsv, blueLb, blueUb) #masks all colors other than blue LED
        
        # Converting image to a binary image 
        _,blueThreshold = cv2.threshold(blueMask[ int(glbl.box[0][1]):int(glbl.box[3][1]), int(glbl.box[0][0]):int(glbl.box[1][0])], 3, 255, cv2.THRESH_BINARY)
        #Set up detector to detect shapes with same colors
        blueDetector, _ = cv2.findContours(blueThreshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(blueDetector) > 0:
            glbl.setStatBlue(True)
            print('Stationary alignment complete. Beginning mobile calibration and alignment.')
            return blueThreshold
        
        cv2.imshow('Threshold', cv2.resize(blueThreshold, (960, 540)))
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

while (True):
    frame = hexFind(glbl)
    bt = feedbackMobMod(glbl)
    
    cv2.imshow('Threshold', cv2.resize(bt, (960, 540)))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    