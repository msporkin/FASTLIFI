#Standard Imports
import cv2
import numpy as np
from scipy.spatial import distance
from imutils import perspective
from header import *
import time
import threading

#Read capture
cap = cv2.VideoCapture(-1)
cap.set(3,1920)
cap.set(4,1080)

#set bounds for LED
ledLit = False

#set bounds for limegreen
lower_bound = np.array([0,70,50])
upper_bound = np.array([80, 180, 240])
offsetMeters = np.array([0,0,0])
font = cv2.FONT_HERSHEY_SIMPLEX

while ledLit == False:
    #printpos(offsetMeters)
    #read frame
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   #converts BRG -> HSV image
    mask = cv2.inRange(hsv, lower_bound, upper_bound)   #masks all colors other than ideal green
    
    #smooths image - chosen over Gaussian Blur for sharpness
    bilateralBlur = cv2.bilateralFilter(mask, 3, 60,60, borderType=cv2.BORDER_REFLECT) 
    
    # Converting image to a binary image 
    _,threshold = cv2.threshold(bilateralBlur, 3, 255, cv2.THRESH_BINARY)
    #Set up detector to detect shapes with same colors
    detector, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Searching through every region selected to find the required polygon. 
    for cnt in detector : 
        area = cv2.contourArea(cnt) 
        # Shortlisting the regions based on area. 
        if area > 100:  
            approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True) 
            # Checking if the no. of sides of the selected region is 7. 
            if(len(approx) == 6):
                offsetMeters, center, ledLit = hex_position(frame, cnt, approx)
                tiltInfo = tilt(approx)
                cv2.putText(frame, str(offsetMeters),(100,500),font,1,(0,0,0),2)
                cv2.putText(frame, tiltInfo,(100,550),font,1,(0,0,0),2)
    # Showing the image along with outlined arrow.
    cv2.imshow('Image', cv2.resize(frame, (960,540)))
    cv2.imshow('mask', cv2.resize(bilateralBlur, (960,540)))
    
     #leave the loop if triggered
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
#Shuts it down
cap.release()
cv2.destroyAllWindows