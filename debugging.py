#ECEN 404 - Michael Sporkin

#Imports custom libraries and threading
from CameraLibrary import *
from MotorLibrary import *
from GVars import *
import threading

glbl = GlbVars() #initializes all global variables in class of setters
statPi = StatPi() #initializes stationary pi class with GPIO designations

#sweep function - turns module a full 180 degrees
def sweepMod(ap1, an1, bp1, bn1, ap2, an2, bp2, bn2, glbl):
    sequences = 0 #tracks "ticks" of the motor
    seqLimit = 2750 #max "ticks" to complete a half rotation
    direction = 'ccw' #initial direction of rotation - clockwise or counterclockwise
    sweepCount = 0 #number of completed sweeps
    sweepNum = 1 #number of sweeps it will perform
    tilted = 'neutral' #tracks current position of module
    snakes = 0
    print('Starting sweep...')
    
    while glbl.esc == False: #will run until quit
        if glbl.sweeping == True: #will run only if in sweeping mode
            while glbl.targetFound == False and sweepCount < sweepNum: #not found and still need to sweep
                if direction == 'ccw' and sequences > -1*seqLimit: #turning ccw and not at limit
                    oneQuickLeftTurn(ap1, an1, bp1, bn1, delayS)
                    sequences = sequences - 1
                    
                elif sequences == -1*seqLimit: #at -90 degrees from center
                    direction = 'cw' #change direction
                    sequences = sequences + 1
                    #Module is tilted up after second ccw rotation, needs to tilt down
                    #   to see the bottom third of steradian range
                    if tilted == 'up':
                        tilted = setTilt(tilted, 'down', ap2, an2, bp2, bn2)
                    time.sleep(delayC)
                    
                elif direction == 'cw' and sequences < seqLimit: #turning cw and not at limit
                    oneQuickRightTurn(ap1, an1, bp1, bn1, delayS)
                    sequences = sequences + 1
                    
                elif sequences == seqLimit: #at 90 degrees from center
                    sequences = sequences - 1
                    direction = 'ccw' #change direction
                    snakes = snakes + 1 #increment number of snake shapes completed this sweep
                    if snakes == 2:
                        sweepCount = sweepCount + 1 #two snakes per sweep
                        snakes = 0
                        #Module is tilted down after final rotation, needs to start tilted neutral
                        #   for next sweep of steradian range
                        if tilted == 'down':
                            tilted = setTilt(tilted, 'neutral', ap2, an2, bp2, bn2)
                    #Module is tilted down after final rotation, needs to start tilted neutral
                    #   for next sweep of steradian range
                    elif tilted == 'down':
                        tilted = setTilt(tilted, 'neutral', ap2, an2, bp2, bn2)
                    #Module is tilted neutral after first cw rotation, needs to tilt up
                    #   to see upper third of steradian range
                    elif tilted == 'neutral':
                        tilted = setTilt(tilted, 'up', ap2, an2, bp2, bn2)
                    time.sleep(delayC)
                    
            if sweepCount >= sweepNum: #if completed all expected sweeps
                print('No target present. Shutting down...') 
                while sequences > 0:
                    oneQuickLeftTurn(ap1, an1, bp1, bn1, delayS)
                    sequences = sequences - 1
                glbl.setEsc(True)
                return
                
            #get really close before fine tuning alignment    
            if glbl.targetFound == True:
                print('Hexagon spotted.')
                time.sleep(delayS)
                #If target right or left of center, will turn in respective direction
                while abs(glbl.centerFrame[0]-glbl.center[0])>10:
                    if (glbl.centerFrame[0] - glbl.center[0]) < 10 and sequences < seqLimit:
                        oneQuickRightTurn(ap1, an1, bp1, bn1, delayS)
                        sequences = sequences + 1
                    elif (glbl.centerFrame[0] - glbl.center[0]) > 10 and sequences > -1*seqLimit:
                        oneQuickLeftTurn(ap1, an1, bp1, bn1, delayS)
                        sequences = sequences - 1
                while abs(glbl.centerFrame[1]-glbl.center[1])>10:
                    if (glbl.centerFrame[1] - glbl.center[1]) < 10 and sequences < seqLimit:
                        oneQuickDownTurn(ap2, an2, bp2, bn2, delayS)                    
                    elif (glbl.centerFrame[1] - glbl.center[1]) > 10 and sequences > -1*seqLimit:
                        oneQuickUpTurn(ap2, an2, bp2, bn2, delayS)
                        
                glbl.setSweeping(False)
                sweepCount = 0
            elif glbl.targetFound == False:    
                print('Full sweep. Target not found.')
                return

#begins full sweep
threading.Thread(target=sweepMod, args = [statPi.ap1, statPi.an1,
    statPi.bp1, statPi.bn1, statPi.ap2, statPi.an2, statPi.bp2, statPi.bn2, glbl]).start()

while glbl.esc == False:
    while glbl.sweeping == True:
        frame = hexFind(glbl)
        # Showing the image along with outlined arrow.
        cv2.imshow('Room Scan', cv2.resize(frame, (960,540)))
        
        #leave the loop if triggered
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    if glbl.sweeping == False and glbl.mobBlue == False:
        print('Sweep complete.')
        printpos(glbl.offsetAngles)

    