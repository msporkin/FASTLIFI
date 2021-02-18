#ECEN 404 - Michael Sporkin

#Standard Imports
import cv2
import numpy as np
from imutils import perspective
from header import *

#Read capture
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1024)

#set bounds for LED
ledLit = False

#set bounds for limegreen
lb = np.array([65, 100, 150])
ub = np.array([90, 255, 255])
font = cv2.FONT_HERSHEY_SIMPLEX

while ledLit == False:
    #read frame
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   #converts BRG -> HSV image
    mask = cv2.inRange(hsv, lb, ub)   #masks all colors other than ideal green
    
    # Converting image to a binary image 
    _,threshold = cv2.threshold(mask, 3, 255, cv2.THRESH_BINARY)
    #Set up detector to detect shapes with same colors
    detector, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Searching through every region selected to find the required polygon. 
    for cnt in detector : 
        area = cv2.contourArea(cnt) 
        # Shortlisting the regions based on area. 
        if area > 200:  
            approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True) 
            # Checking if the no. of sides of the selected region is 7. 
            if (len(approx) == 6):        
                #finds rectangle vertices around area, then orders them clockwise
                #   starting at top left
                box = np.array(cv2.boxPoints(cv2.minAreaRect(cnt)))
                (topLeft, topRight, bottomRight, bottomLeft) = perspective.order_points(box)
                
                #finds horizontal midpoints along top and bottom and draws
                leftMiddle = midpoint(topLeft,bottomLeft)
                rightMiddle = midpoint(topRight, bottomRight)
                
                #finds width in pixels of hexagon
                wp = rightMiddle[0] - leftMiddle[0]
                
                cv2.drawContours(frame, [approx], 0, (0, 0, 255), 3)
                cv2.line(frame, leftMiddle, rightMiddle, (255, 0, 0), 2)
                cv2.putText(frame, str(wp),(100,500),font,1,(0,0,0),2)
                
    # Showing the image along with outlined arrow.
    cv2.imshow('Image', cv2.resize(frame, (960,540)))
    #cv2.imshow('Mask', cv2.resize(mask, (960,540)))
    
     #leave the loop if triggered
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
#Shuts it down
cap.release()
cv2.destroyAllWindows