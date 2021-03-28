#ECEN 404 - Michael Sporkin

#Imports custom libraries and threading
from CameraLibrary import *
from MotorLibrary import *
from GVars import *
import threading

glbl = GlbVars() #initializes all global variables in class of setters
statPi = StatPi() #initializes stationary pi class with GPIO designations

#begins full sweep
threading.Thread(target=sweep, args = [statPi.ap1, statPi.an1,
    statPi.bp1, statPi.bn1, statPi.ap2, statPi.an2, statPi.bp2, statPi.bn2, glbl]).start()

printpos(glbl.offsetAngles)
while glbl.mobBlue == False:
    frame = hexFind(glbl)
    # Showing the image along with outlined arrow.
    cv2.imshow('Room Scan', cv2.resize(frame, (960,540)))
    
    if glbl.sweeping == False:
        print('Sweep complete. Beginning alignment.')
        printpos(glbl.offsetAngles)
        cv2.destroyWindow('Room Scan')
        
        #Calibrate Motors
        Calibrate(statPi.ap1, statPi.an1, statPi.bp1, statPi.bn1, statPi.ap2, statPi.an2,
                  statPi.bp2, statPi.bn2, delayC)
        print('Calibration complete')
        
        #Calculate new offset after calibration and align
        frame = hexFind(glbl)
        
        printpos(glbl.offsetAngles)
        Align(glbl.offsetAngles, statPi.ap1, statPi.an1, statPi.bp1, statPi.bn1, statPi.ap2,
              statPi.an2, statPi.bp2, statPi.bn2)
        
        #Calculate and show new offset to confirm alignment
        while glbl.mobBlue == False:
            frame = hexFind(glbl)
            
            cv2.imshow('Target Aligned', cv2.resize(frame, (960,540)))
            
            glbl.setStatBlue(True)
            statPi.blueToggle(glbl.statBlue)
            statPi.vcselToggle(True)
            feedbackStat(glbl)
            
            #leave the loop if triggered
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
     #leave the loop if triggered
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Shuts it down
cap.release()
cv2.destroyAllWindows
