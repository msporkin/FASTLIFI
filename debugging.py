#ECEN 404 - Michael Sporkin

#Imports custom libraries and threading
from CameraLibrary import *
from MotorLibrary import *
from MobileMotorLibrary import *
from GVars import *
import threading

glbl = GlbVars() #initializes all global variables in class of setters
mobPi = MobPi() #initializes stationary pi class with GPIO designations

while (True):
    frame, mask = hexFind(glbl)
    cv2.imshow('Room Scan', mask)
        
    #leave the loop if triggered
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
