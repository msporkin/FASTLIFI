#ECEN 404 - Michael Sporkin

#Imports custom libraries and threading
from CameraLibrary import *
from MotorLibrary import *
from GVars import *
import threading

glbl = GlbVars() #initializes all global variables in class of setters
statPi = StatPi() #initializes stationary pi class with GPIO designations

#escape sits idle waiting for input
threading.Thread(target=escape, args=[glbl]).start()

#begins full sweep
threading.Thread(target=sweep, args = [statPi.ap1, statPi.an1,
    statPi.bp1, statPi.bn1, statPi.ap2, statPi.an2, statPi.bp2, statPi.bn2, glbl]).start()

while glbl.esc == False:
    if glbl.sweeping == True:
        statPi.blueToggle(False)
        glbl.setStatBlue(False)
        statPi.vcselToggle(False)
    
    while glbl.sweeping == True:
        statPi.blueToggle(False)
        frame = hexFind(glbl)
        # Showing the image along with outlined arrow.
        cv2.imshow('Room Scan', cv2.resize(frame, (960,540)))
        
        #leave the loop if triggered
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    if glbl.sweeping == False and glbl.mobBlue == False:
        print('Sweep complete.')
        printpos(glbl.offsetAngles)
        cv2.destroyWindow('Room Scan')
        
    #Calibrate Motors if done with a sweep
    if glbl.sweeping == False and glbl.calibrated == False:
        """
        print('Beginning calibration.')
        #Calibrate Motors
        Calibrate(statPi.ap1, statPi.an1, statPi.bp1, statPi.bn1, statPi.ap2, statPi.an2,
                  statPi.bp2, statPi.bn2, delayC)
        print('Calibration complete')
        """
        glbl.setCalibrated(True)
        """
        time.sleep(3)
        #Calculate new offset after calibration and align
        printpos(glbl.offsetAngles)
        Align(glbl.offsetAngles, statPi.ap1, statPi.an1, statPi.bp1, statPi.bn1, statPi.ap2,
              statPi.an2, statPi.bp2, statPi.bn2)
        """
        glbl.setStatBlue(True)
        statPi.blueToggle(glbl.statBlue)
        statPi.vcselToggle(True)
        print('Waiting for mobile blue LED to indicate link establishment.')
    
    #Calculate and show new offset to confirm alignment
    while glbl.mobBlue == False:
        frame = hexFind(glbl)
        cv2.imshow('Target Aligned', cv2.resize(frame, (960,540)))
        
        feedbackStat(glbl, statPi)
        
        #leave the loop if triggered
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    while glbl.link == True and glbl.esc == False:
        frame = hexFind(glbl)
        cv2.imshow('Target Aligned', cv2.resize(frame, (960,540)))
        
        #leave the loop if triggered
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        feedbackStat(glbl, statPi)
        
        
    if glbl.targetFound == False and glbl.link == False:
        glbl.setMobBlue(False)
        glbl.setStatBlue(False)
        statPi.blueToggle(False)
        statPi.vcselToggle(False)
        glbl.setCalibrated(False)
        cv2.destroyWindow('Target Aligned')
