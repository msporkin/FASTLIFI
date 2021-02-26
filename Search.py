#ECEN 404 - Michael Sporkin

#Imports custom libraries and threading
from CameraLibrary import *
from MotorLibrary import *
import threading

#initialize search variables
ledLit = False
offsetAngles = np.array([0,0,0])
global targetFound
targetFound = False
global sweeping
sweeping = True

statPi = StatPi() #initializes stationary pi class with GPIO designations

#sweep function - turns module a full 180 degrees
def sweep(ap1, an1, bp1, bn1, delay):
    global targetFound
    sequences = 0
    while targetFound == False and sequences < 7000:
        oneQuickRightTurn(ap1, an1, bp1, bn1, delay)
        sequences = sequences + 1
    if targetFound == True:
        print('Hexagon spotted.')
        global center #center of the hexagon
        while abs(centerFrame[0]-center[0])>40 and sequences < 7000:
            oneQuickRightTurn(ap1, an1, bp1, bn1, delay)
            sequences = sequences + 1
        global sweeping
        sweeping = False
        return
    if targetFound == False:    
        print('Full 180 degree sweep. Target not found.')
        return

#begins full sweep
threading.Thread(target=sweep, args = [statPi.ap1, statPi.an1,
                    statPi.bp1, statPi.bn1, delayS]).start()

printpos(offsetAngles)
while ledLit == False:
    #read frame
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   #converts BRG -> HSV image
    mask = cv2.inRange(hsv, lb, ub)   #masks all colors other than ideal green
    
    #smooths image - chosen over Gaussian Blur for sharpness
    #mask = cv2.bilateralFilter(mask, 3, 60,60, borderType=cv2.BORDER_REFLECT)
    
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
                targetFound = True
                offsetAngles, center = hex_position(frame, cnt, approx)
                #tiltInfo = tilt(approx)
        
                cv2.putText(frame, str(offsetAngles),(100,500),font,1,(0,0,0),2)
                #cv2.putText(frame, tiltInfo,(100,550),font,1,(0,0,0),2)
                
    # Showing the image along with outlined arrow.
    cv2.imshow('Room Scan', cv2.resize(frame, (960,540)))
    
    if sweeping == False:
        print('Sweep complete. Beginning alignment.')
        printpos(offsetAngles)
        cv2.destroyWindow('Room Scan')
        
        #Calibrate Motors
        Calibrate(statPi.ap1, statPi.an1, statPi.bp1, statPi.bn1, statPi.ap2, statPi.an2,
                  statPi.bp2, statPi.bn2, delayC)
        print('Calibration complete')
        
        #Calculate new offset after calibration and align
        frame, cnt, approx = hex_find()
        offsetAngles, center = hex_position(frame, cnt, approx)
        printpos(offsetAngles)
        Align(offsetAngles, statPi.ap1, statPi.an1, statPi.bp1, statPi.bn1, statPi.ap2,
              statPi.an2, statPi.bp2, statPi.bn2)
        
        #Calculate and show new offset to confirm alignment
        while (True):
            frame, cnt, approx = hex_find()
            offsetAngles, _ = hex_position(frame, cnt, approx)
            cv2.imshow('Target Aligned', cv2.resize(frame, (960,540)))
            #leave the loop if triggered
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        
     #leave the loop if triggered
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Shuts it down
cap.release()
cv2.destroyAllWindows