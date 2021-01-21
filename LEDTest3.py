#Standard Imports
import cv2
import numpy as np
from scipy.spatial import distance
import imutils
from skimage.metrics import structural_similarity
import time
import threading
from header import *
from gpiozero import LED

#Read capture
cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)

#set bounds for LED
led_lower_bound = np.array([55, 1,240])
led_upper_bound = np.array([70, 15, 255])
ledLit = False

def backgroundImage():
    ret1, frame1 = cap.read()
    background_hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)   #converts BRG -> GRAY image
    global background_mask
    background_mask = cv2.inRange(background_hsv, led_lower_bound, led_upper_bound)   #masks all colors other than LED yellow/white

global background_mask
backgroundImage()

while ledLit == False:
    #read frame
    ret, frame = cap.read()
    led_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   #converts BRG -> HSV image
    led_blur = cv2.bilateralFilter(led_hsv, 5, 80, 40)
    led_smooth = cv2.inRange(led_hsv, led_lower_bound, led_upper_bound)   #masks all colors other than LED yellow/white

    diff = led_smooth - background_mask
    diff = (diff*255).astype('uint8')
    _, diff_thresh = cv2.threshold(diff, 0, 100, cv2.THRESH_BINARY_INV)
    diff_thresh = cv2.bilateralFilter(diff_thresh, 3, 100,60, borderType=cv2.BORDER_REFLECT) 
    
    #find contours
    diff_cnts, _ = cv2.findContours(diff_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c1 in diff_cnts:
        _center, rad = cv2.minEnclosingCircle(c1)
        cv2.circle(frame, (int(_center[0]), int(_center[1])), int(rad), (0,0,255), 2)
        if (.75*3.14*rad*rad) < cv2.contourArea(c1):
            print(_center)
            cv2.circle(frame, (int(_center[0]), int(_center[1])), int(rad), (0,0,255), 2)
            ledLit = True
    cv2.imshow('Difference Highlighter', cv2.resize(diff_thresh, (960,540)))
    cv2.imshow('Circles', cv2.resize(frame, (960,540)))
    cv2.imshow('LED', cv2.resize(led_smooth, (960,540)))
     #leave the loop if triggered
    if cv2.waitKey(1) & 0xFF == ord('q'):
        ledLit = True

#Shuts it down
print("LED seen. Shutting down...")
cap.release()
cv2.destroyAllWindows
