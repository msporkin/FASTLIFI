#Standard Imports
import cv2
import math
import numpy as np
from scipy.spatial import distance as dist
from imutils import perspective

#Camera specific variables
font = cv2.FONT_HERSHEY_SIMPLEX #font on image
#set bounds for backlit green
lb = np.array([65, 100, 100])
ub = np.array([90, 255, 255])

#Read capture
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1024)

#Calculates z distance from experimentally defined function
def z_distance(wp):
    z = 143.72*pow(wp, -.976)
    return float(z)

#Calculates radian angle offset from x axis
def theta_offset(z, cx, center, ppm):
    x = (cx - center)/ppm
    theta = math.atan(x/z)
    return theta

#calculates radian angle offset from y axis
def phi_offset(z, cy, center, ppm):
    y = (center - cy)/ppm
    phi = math.atan(y/z)
    return phi

#midpoint of two points
def midpoint(left, right):
    x = int((left[0]+right[0])/2)
    y = int((left[1]+right[1])/2)
    return (x,y)

def hexFind(glbl):
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
        if area > 120:  
            approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True) 
            # Checking if the no. of sides of the selected region is 7. 
            if (len(approx) == 6):
                glbl.setTargetFound(True)
                hex_position(frame, cnt, approx, glbl)
                cv2.putText(frame, str(glbl.offsetAngles),(100,500),font,1,(0,0,0),2)
                
    return frame

def hex_position(frame, cnt, approx, glbl):
    
    #finds rectangle vertices around area, then orders them clockwise
    #   starting at top left
    box = np.array(cv2.boxPoints(cv2.minAreaRect(cnt)))
    (topLeft, topRight, bottomRight, bottomLeft) = perspective.order_points(box)
    glbl.setBox(topLeft, topRight, bottomRight, bottomLeft)
    
    #finds horizontal midpoints along top and bottom and draws
    leftMiddle = midpoint(topLeft,bottomLeft)
    rightMiddle = midpoint(topRight, bottomRight)
    
    #finds width in pixels of hexagon
    wp = dist.euclidean(leftMiddle, rightMiddle)
    
    #pixels per meter
    ppm = wp/.1143 #width in cm = 11.43
    
    #finds center
    cx, cy = midpoint(leftMiddle, rightMiddle)
    glbl.setCenter(cx, cy)
    
    #finds z
    z = z_distance(wp)
    
    #finds theta and phi angle offset using trig ratios
    theta = theta_offset(z, cx, glbl.centerFrame[0], ppm)
    phi = phi_offset(z, cy, glbl.centerFrame[1], ppm)
    
    cv2.drawContours(frame, [approx], 0, (0, 0, 255), 3) #outlines hexagon
    cv2.line(frame, leftMiddle, rightMiddle, (255, 0, 0), 2) #draws line across width
    cv2.line(frame, glbl.center, glbl.centerFrame, (0, 255, 0), 2) #draws line to center of frame
    
    glbl.setOffsetAngles([round(z,3),round(theta,3),round(phi,3)])
    
    return

def printpos(offset):
    if offset[0] == 0 and offset[1] == 0 and offset[2] == 0:
        print("Searching...")
    else:
        print('Target positioned at [z,theta,phi]: '+str(offset))
        
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

def feedbackMob(glbl):
    blueLb = np.array([110, 150, 150])
    blueUb = np.array([130, 255, 255])
    
    _, frame1 = cap.read()
    blueHsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    blueMask = np.zeros(frame1.shape, np.uint8) # makes initial array of zeros in size of array
    
    #Mask out everything in the image except for one half the pixel height of the hexagon above the target
    blueMask[ int(glbl.box[0][1]):int(glbl.box[3][1]), int(glbl.box[0][0]):int(glbl.box[1][0]), :
               ] = frame1[ int(glbl.box[0][1]):int(glbl.box[3][1]), int(glbl.box[0][0]):int(glbl.box[1][0]), : ]
    blueMask = cv2.inRange(blueHsv, blueLb, blueUb) #masks all colors other than blue LED
    
    # Converting image to a binary image 
    _,blueThreshold = cv2.threshold(blueMask[int(glbl.box[0][1]):int(glbl.box[3][1]),
                        int(glbl.box[0][0]):int(glbl.box[1][0])], 3, 255, cv2.THRESH_BINARY)
    #Set up detector to detect shapes with same colors
    blueDetector, _ = cv2.findContours(blueThreshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(blueDetector) > 0:
        glbl.setStatBlue(True)
        print('Stationary alignment complete. Beginning mobile calibration and alignment.')
        return
    
def feedbackStat(glbl):
    blueLb = np.array([110, 150, 150])
    blueUb = np.array([130, 255, 255])
    
    _, frame1 = cap.read()
    blueHsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    blueMask = np.zeros(frame1.shape, np.uint8) # makes initial array of zeros in size of array
    
    #Mask out everything in the image except for one half the pixel height of the hexagon above the target
    blueMask[ int(glbl.box[0][1]):int(glbl.box[3][1]), int(glbl.box[0][0]):int(glbl.box[1][0]), :
               ] = frame1[ int(glbl.box[0][1]):int(glbl.box[3][1]), int(glbl.box[0][0]):int(glbl.box[1][0]), : ]
    blueMask = cv2.inRange(blueHsv, blueLb, blueUb) #masks all colors other than blue LED
    
    # Converting image to a binary image 
    _,blueThreshold = cv2.threshold(blueMask[int(glbl.box[0][1]):int(glbl.box[3][1]),
                        int(glbl.box[0][0]):int(glbl.box[1][0])], 3, 255, cv2.THRESH_BINARY)
    #Set up detector to detect shapes with same colors
    blueDetector, _ = cv2.findContours(blueThreshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(blueDetector) > 0:
        glbl.setMobBlue(True)
        print('Representative link established on mobile module')
        return
    
    # Showing the feedback frame
    #cv2.imshow('Blue Mask', cv2.resize(blueMask, (960,540)))
    
