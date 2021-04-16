#Michael Sporkin, Amanda Aboujaoude, Ryan Quinn - ECEN 404 FAST LiFi

#Imports custom libraries and threading
from CameraLibrary import *
from MotorLibrary import *
from MobileMotorLibrary import *
from ADCandTestLibrary import *
from GVars import *
import threading

glbl = GlbVars() #initializes all global variables in class of setters
mobPi = MobPi() #initializes stationary pi class with GPIO designations
name = input('Name the test file: ')

#escape sits idle waiting for input
threading.Thread(target=escape, args=[glbl]).start()

#begins full sweep
threading.Thread(target=sweep, args = [mobPi.ap1, mobPi.an1, mobPi.bp1, mobPi.bn1,
                        mobPi.ap2, mobPi.an2, mobPi.bp2, mobPi.bn2, glbl]).start()

#prints the current state whenever photodetector notices change and records voltages
threading.Thread(target=pdcGraph, args=[name, glbl]).start()
threading.Thread(target=printAS, args=[glbl]).start()

while glbl.esc == False:
    while glbl.sweeping == True:
        frame = hexFind(glbl)
        # Showing the image along with outlined arrow.
        cv2.imshow('Room Scan', frame)
        
        #leave the loop if triggered
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if glbl.sweeping == False:
            print('Sweep complete.')
            printpos(glbl.offsetAngles)
            cv2.destroyWindow('Room Scan')
      
    #Calibrate Motors if done with a sweep
    if glbl.sweeping == False and glbl.calibrated == False:
        print('Beginning calibration.')
        Calibrate(mobPi.ap1, mobPi.an1, mobPi.bp1, mobPi.bn1, mobPi.ap2, mobPi.an2,
                  mobPi.bp2, mobPi.bn2, delayC)
        glbl.setCalibrated(True)
        print('Calibration complete. Waiting for feedback to initiate alignment.')
        time.sleep(5)
    
    while glbl.statBlue == False:
        feedbackMob(glbl)
    
    if glbl.statBlue == True and glbl.link == False and glbl.sweeping == False:
        #Calculate new offset after calibration and align
        frame = hexFind(glbl)
        printpos(glbl.offsetAngles)
        Align(glbl.offsetAngles, mobPi.ap1, mobPi.an1, mobPi.bp1, mobPi.bn1, mobPi.ap2, mobPi.an2,
                  mobPi.bp2, mobPi.bn2)

        #Show new offset to confirm alignment
        frame = hexFind(glbl)
        cv2.imshow('Target Centered', cv2.resize(frame, (960,540))) 
        
        mobPi.blueToggle(glbl.mobBlue)
        servoSnake(mobPi.servoX, mobPi.servoY, glbl)
        mobPi.blueToggle(glbl.mobBlue)
    
    while glbl.link == True:
        feedbackMob(glbl)
        if glbl.targetFound == False:
            glbl.setStatBlue(False)
            glbl.setMobBlue(False)
            mobPi.blueToggle(glbl.mobBlue)
            cv2.destroyWindow('Target Centered')