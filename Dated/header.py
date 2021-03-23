#Standard Imports
import cv2
import numpy as np
import threading
import time
from scipy.spatial import distance as dist
from imutils import perspective

def x_distance(z, pxl):
    xh = 1.15 #width in x direction in meters
    if pxl < 960:
        return float(-xh/1920*z*pxl)
    else:
        return float(xh/1920*z*pxl)

def z_distance(pxl):
    ratio = .68/1080 # meters/pixel
    h = .0635 #cm = 4 inches
    return float((h/ratio)/pxl)

def y_distance(z, pxl):
    yh = .7 #length in y direction in meters
    if pxl < 540:
        return float(yh/1080*z*pxl)
    else:
        return float(-yh/1080*z*pxl)

def midpoint(left, right):
    x = int((left[0]+right[0])/2)
    y = int((left[1]+right[1])/2)
    return (x,y)

def hex_position(frame, cnt, approx):
    
    #finds rectangle vertices around area, then orders them clockwise
    #   starting at top left
    box = np.array(cv2.boxPoints(cv2.minAreaRect(cnt)))
    (topLeft, topRight, bottomLeft, bottomRight) = perspective.order_points(box)
    
    #finds horizontal midpoints along top and bottom and draws
    topMiddle = midpoint(topLeft,topRight)
    bottomMiddle = midpoint(bottomLeft, bottomRight)
    
    #finds z using pixel ratio from h
    h = dist.euclidean(topMiddle, bottomMiddle)
    z = z_distance(h)
    
    #finds x and y offset using trig ratios
    center = midpoint(topMiddle, bottomMiddle)
    y = y_distance(z, (540-center[1]))
    x = x_distance(z, (960-center[0]))
    
    #Checks if LED is on behind the hexagon
    #ledLit = ledSearch(frame, topLeft, topRight, bottomLeft, bottomRight, center)
    
    cv2.drawContours(frame, [approx], 0, (0, 0, 255), 3)
    cv2.line(frame, topMiddle, bottomMiddle, (255, 0, 0), 2)
    cv2.line(frame, center, (960,540), (0, 255, 0), 2)
    
    offsetMeters = [round(x,3),round(y,3),round(z,3)]
    
    return offsetMeters, center#, ledLit

def printpos(offsetMeters):
    if offsetMeters[0] == 0 and offsetMeters[1] == 0 and offsetMeters[2] == 0:
        print("Searching...")
    else:
        print('[x,y,z]: '+str(offsetMeters))
        
def tilt(approx):
    #Reorganizes array into xy pixel pairs, starting in bottom left corner
    approx = approx.ravel()
    i = 0
    j = 0
    vertices = [0, 0, 0, 0, 0, 0]
    while j < 6:
        vertices[j] = [approx[i], approx[i+1]]
        j = j+1
        i = i+2

    #finds length of edges
    bottomLeftEdge = dist.euclidean(vertices[0], vertices[1])
    topLeftEdge = dist.euclidean(vertices[1],vertices[2])
    topEdge = dist.euclidean(vertices[2], vertices[3])
    topRightEdge = dist.euclidean(vertices[3],vertices[4])
    bottomRightEdge = dist.euclidean(vertices[4],vertices[5])
    bottomEdge = dist.euclidean(vertices[5], vertices[0])

    tiltInfo = 'Tilted:'

    if .97*(topRightEdge+topEdge+topLeftEdge) > (bottomRightEdge+bottomEdge+bottomLeftEdge):
        tiltInfo = tiltInfo+' Up'
    elif (topRightEdge+topEdge+topLeftEdge) < .97*(bottomRightEdge+bottomEdge+bottomLeftEdge):
        tiltInfo = tiltInfo+' Down'
    if (bottomLeftEdge+topLeftEdge) < .97*(bottomRightEdge+topRightEdge):
        tiltInfo = tiltInfo+' Left'
    elif .97*(bottomLeftEdge+topLeftEdge) > (bottomRightEdge+topRightEdge):
        tiltInfo = tiltInfo+' Right'
        
    return tiltInfo
"""
def ledSearch(frame, topLeft, topRight, bottomLeft, bottomRight, center):
    #set bounds for LED behind Hexagon
    led_lower_bound = np.array([0, 0, 0])
    led_upper_bound = np.array([40, 40, 250])
    
    mask = np.zeros(frame.shape, np.uint8)
    mask[int(topLeft[1]):int(bottomLeft[1]), int(topLeft[0]):int(topRight[0]), :] = frame[int(topLeft[1]):int(bottomLeft[1]), int(topLeft[0]):int(topRight[0]), :]
    mask = cv2.inRange(mask, led_lower_bound, led_upper_bound)   #masks all colors other than LED yellow/white
    
    cv2.imshow('Hexagon Mask', cv2.resize(mask, (960,540)))
    
    if mask[center[1], center[0]] == 0:
        ledLit = True
        print('LED seen. Shutting down...')
    else:
        ledLit = False
        
    return ledLit
"""
def ledSearch(frame, topLeft, topRight, bottomLeft, bottomRight, center):
    #set bounds for LED behind Hexagon
    led_lower_bound = np.array([0, 0, 0])
    led_upper_bound = np.array([40, 40, 250])
    
    mask = np.zeros(frame.shape, np.uint8)
    mask[int(topLeft[1]):int(bottomLeft[1]), int(topLeft[0]-180):int(topRight[0]-180), :] = frame[int(topLeft[1]+40):int(bottomLeft[1]+40), int(topLeft[0]):int(topRight[0]), :]
    cv2.rectangle(frame, (int(topLeft[1]),int(topLeft[0]-180)), (int(bottomRight[1]),int(bottomRight[0]-180)), (255, 0,0), 3)
    mask = cv2.inRange(mask, led_lower_bound, led_upper_bound)   #masks all colors other than LED yellow/white
    
    cv2.imshow('Hexagon Mask', cv2.resize(mask, (960,540)))
    
    if mask[center[1]-180, center[0]] == 1:
        ledLit = True
        print('LED seen. Shutting down...')
    else:
        ledLit = False
        
    return ledLit
    
