import RPi.GPIO as GPIO
import time
import math

#Broadcom channel definition of GPIO pins (using designated GPIO pin number)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) #Disable warnings

#Set motor variables
delayC = 2 #Time delay in ms
delayS = .01 #Time delay - sweep
winding_i1 = 0 #Initialize windings
winding_i2 = 0 #Initialize windings
calNum = 3 #calibration number

class StatPi:
    def __init__(self): 
        #Defining enable pins on first L298N to GPIOs on Raspberry Pi
        self.ENA1 = 18
        self.ENB1 = 22

        #Defining enable pins on second L298N to GPIOs on Raspberry Pi
        self.ENA2 = 25
        self.ENB2 = 16

        #Defining winding pins on first L298N to GPIOs on Raspberry Pi
        self.ap1 = 23 #int1
        self.an1 = 24 #int2
        self.bp1 = 4  #int3
        self.bn1 = 17 #int4

        #Defining winding pins on second L298N to GPIOs on Raspberry Pi
        self.ap2 = 27 #int1
        self.an2 = 13 #int2
        self.bp2 = 5  #int3
        self.bn2 = 6  #int4


        #Defining all GPIOs to be output
        GPIO.setup(self.ENA1, GPIO.OUT)
        GPIO.setup(self.ENB1, GPIO.OUT)
        GPIO.setup(self.ap1, GPIO.OUT)
        GPIO.setup(self.an1, GPIO.OUT)
        GPIO.setup(self.bp1, GPIO.OUT)
        GPIO.setup(self.bn1, GPIO.OUT)
        GPIO.setup(self.ENA2, GPIO.OUT)
        GPIO.setup(self.ENB2, GPIO.OUT)
        GPIO.setup(self.ap2, GPIO.OUT)
        GPIO.setup(self.an2, GPIO.OUT)
        GPIO.setup(self.bp2, GPIO.OUT)
        GPIO.setup(self.bn2, GPIO.OUT)

        #Defining ENA and ENB to be true/1 to enable A+/A- and B+/B- ports
        GPIO.output(self.ENA1, True)
        GPIO.output(self.ENB1, True)
        GPIO.output(self.ENA2, True)
        GPIO.output(self.ENB2, True)

#Defining calibration for horizontal L298N
def CalibrateX(ap1, state1, an1, state2, bp1, state3, bn1, state4):
    GPIO.output(ap1, state1)
    GPIO.output(an1, state2)
    GPIO.output(bp1, state3)
    GPIO.output(bn1, state4)
    global winding_i1
    winding_i1 = 0

#Defining calibration for vertical L298N
def CalibrateY(ap2, State1, an2, State2, bp2, State3, bn2, State4):
    GPIO.output(ap2, State1)
    GPIO.output(an2, State2)
    GPIO.output(bp2, State3)
    GPIO.output(bn2, State4)
    global winding_i2
    winding_i2 = 0
    

def Calibrate(ap1, an1, bp1, bn1, ap2, an2, bp2, bn2, delay):
    for rLeft in range (0, calNum):
        CalibrateX(ap1, 1, an1, 0, bp1, 1, bn1, 0)
        time.sleep(delay)
        CalibrateX(ap1, 0, an1, 1, bp1, 1, bn1, 0)
        time.sleep(delay)
        CalibrateX(ap1, 0, an1, 1, bp1, 0, bn1, 1)
        time.sleep(delay)
        CalibrateX(ap1, 1, an1, 0, bp1, 0, bn1, 1)
        time.sleep(delay)

    for rRight in range (0, calNum):
        CalibrateX(ap1,0,an1,1,bp1,0,bn1,1)
        time.sleep(delay)
        CalibrateX(ap1,0,an1,1,bp1,1,bn1,0)
        time.sleep(delay)
        CalibrateX(ap1,1,an1,0,bp1,1,bn1,0)
        time.sleep(delay)
        CalibrateX(ap1,1,an1,0,bp1,0,bn1,1)
        time.sleep(delay)

    for rDown in range (0, calNum):
        CalibrateY(ap2,1,an2,0,bp2,1,bn2,0)
        time.sleep(delay)
        CalibrateY(ap2,0,an2,1,bp2,1,bn2,0)
        time.sleep(delay)
        CalibrateY(ap2,0,an2,1,bp2,0,bn2,1)
        time.sleep(delay)
        CalibrateY(ap2,1,an2,0,bp2,0,bn2,1)
        time.sleep(delay)

    for rUp in range (0, calNum):
        CalibrateY(ap2,0,an2,1,bp2,0,bn2,1)
        time.sleep(delay)
        CalibrateY(ap2,0,an2,1,bp2,1,bn2,0)
        time.sleep(delay)
        CalibrateY(ap2,1,an2,0,bp2,1,bn2,0)
        time.sleep(delay)
        CalibrateY(ap2,1,an2,0,bp2,0,bn2,1)
        time.sleep(delay)

#Defining one cycle in clockwise direction(1.8 degree step) for first L298N
def oneTickRight(ap1, an1, bp1, bn1):
    global winding_i1
    if winding_i1 > 3:
        winding_i1 = 0 
    if winding_i1 == 0:
          GPIO.output(ap1, 0)
          GPIO.output(an1, 1)
          GPIO.output(bp1, 0)
          GPIO.output(bn1, 1)
          time.sleep(delayC)
    elif winding_i1 == 1:      
          GPIO.output(ap1, 0)
          GPIO.output(an1, 1)
          GPIO.output(bp1, 1)
          GPIO.output(bn1, 0)
          time.sleep(delayC)
    elif winding_i1 == 2:      
          GPIO.output(ap1, 1)
          GPIO.output(an1, 0)
          GPIO.output(bp1, 1)
          GPIO.output(bn1, 0)
          time.sleep(delayC)
    elif winding_i1 == 3:      
          GPIO.output(ap1, 1)
          GPIO.output(an1, 0)
          GPIO.output(bp1, 0)
          GPIO.output(bn1, 1)
          time.sleep(delayC)
    winding_i1 = winding_i1 + 1
    
#Defining one cycle in counterclockwise direction(1.8 degree step) for first L298N
def oneTickLeft(ap1, an1, bp1, bn1):
    global winding_i1
    if winding_i1 > 3:
        winding_i1 = 0 
    if winding_i1 == 0:
          GPIO.output(ap1, 1)
          GPIO.output(an1, 0)
          GPIO.output(bp1, 1)
          GPIO.output(bn1, 0)
          time.sleep(delayC)
    elif winding_i1 == 1:      
          GPIO.output(ap1, 0)
          GPIO.output(an1, 1)
          GPIO.output(bp1, 1)
          GPIO.output(bn1, 0)
          time.sleep(delayC)
    elif winding_i1 == 2:      
          GPIO.output(ap1, 0)
          GPIO.output(an1, 1)
          GPIO.output(bp1, 0)
          GPIO.output(bn1, 1)
          time.sleep(delayC)
    elif winding_i1 == 3:      
          GPIO.output(ap1, 1)
          GPIO.output(an1, 0)
          GPIO.output(bp1, 0)
          GPIO.output(bn1, 1)
          time.sleep(delayC)
    winding_i1 = winding_i1 + 1

#Defining one cycle in clockwise direction(1.8 degree step) for second L298N
def oneTickUp(ap2, an2, bp2, bn2):
    global winding_i2
    if winding_i2 > 3:
        winding_i2 = 0 
    if winding_i2 == 0:
          GPIO.output(ap2, 0)
          GPIO.output(an2, 1)
          GPIO.output(bp2, 0)
          GPIO.output(bn2, 1)
          time.sleep(delayC)
    elif winding_i2 == 1:      
          GPIO.output(bp2, 0)
          GPIO.output(bn2, 1)
          GPIO.output(bp2, 1)
          GPIO.output(bn2, 0)
          time.sleep(delayC)
    elif winding_i2 == 2:      
          GPIO.output(ap2, 1)
          GPIO.output(an2, 0)
          GPIO.output(bp2, 1)
          GPIO.output(bn2, 0)
          time.sleep(delayC)
    elif winding_i2 == 3:      
          GPIO.output(ap2, 1)
          GPIO.output(an2, 0)
          GPIO.output(bp2, 0)
          GPIO.output(bn2, 1)
          time.sleep(delayC)
    winding_i2 = winding_i2 + 1
    
#Defining one cycle in clockwise direction(1.8 degree step) for second L298N
def oneTickDown(ap2, an2, bp2, bn2):
    global winding_i2
    if winding_i2 > 3:
        winding_i2 = 0 
    if winding_i2 == 0:
          GPIO.output(ap2, 1)
          GPIO.output(an2, 0)
          GPIO.output(bp2, 1)
          GPIO.output(bn2, 0)
          time.sleep(delayC)
    elif winding_i2 == 1:      
          GPIO.output(bp2, 0)
          GPIO.output(bn2, 1)
          GPIO.output(bp2, 1)
          GPIO.output(bn2, 0)
          time.sleep(delayC)
    elif winding_i2 == 2:      
          GPIO.output(ap2, 0)
          GPIO.output(an2, 1)
          GPIO.output(bp2, 0)
          GPIO.output(bn2, 1)
          time.sleep(delayC)
    elif winding_i2 == 3:      
          GPIO.output(ap2, 1)
          GPIO.output(an2, 0)
          GPIO.output(bp2, 0)
          GPIO.output(bn2, 1)
          time.sleep(delayC)
    winding_i2 = winding_i2 + 1
    
#2/18 - 180 degrees in 7000 clicks (clock-limited movements)
#2/19 - 180 degrees in 500 clicks (continuous)
def fullTurn(ap1, an1, bp1, bn1, delay):     
    for cs in range (0,5):
        print(str(cs))
        for c1 in range (0, 100):
            CalibrateX(ap1, 0, an1, 1, bp1, 0, bn1, 1)
            time.sleep(delay)
            CalibrateX(ap1, 0, an1, 1, bp1, 1, bn1, 0)
            time.sleep(delay)
            CalibrateX(ap1, 1, an1, 0, bp1, 1, bn1, 0)
            time.sleep(delay)
            CalibrateX(ap1, 1, an1, 0, bp1, 0, bn1, 1)
            time.sleep(delay)
    print('Full 180 degree sweep')
        
#2/18 - 45 degrees in 1200 clicks
def fullTilt(ap2, an2, bp2, bn2, delay):     
    for cs in range (0,12):
        for c1 in range (0, 100):
            CalibrateY(ap2, 0, an2, 1, bp2, 0, bn2, 1)
            time.sleep(delay)
            CalibrateY(ap2, 0, an2, 1, bp2, 1, bn2, 0)
            time.sleep(delay)
            CalibrateY(ap2, 1, an2, 0, bp2, 1, bn2, 0)
            time.sleep(delay)
            CalibrateY(ap2, 1, an2, 0, bp2, 0, bn2, 1)
            time.sleep(delay)
    for cs in range (0, 26):
        for c2 in range (0,100):
            CalibrateY(ap2, 1, an2, 0, bp2, 1, bn2, 0)
            time.sleep(delay)
            CalibrateY(ap2, 0, an2, 1, bp2, 1, bn2, 0)
            time.sleep(delay)
            CalibrateY(ap2, 0, an2, 1, bp2, 0, bn2, 1)
            time.sleep(delay) 
            CalibrateY(ap2, 1, an2, 0, bp2, 0, bn2, 1)
            time.sleep(delay)
    print('Full tilt sweep complete')
    
#Using empirical data from fullTurn, it was shown that 500 step series turn 180 degrees
#   500 step sseries/180 degrees = 2.7778 step sseries/degree, so multiplying the desired
#   degrees by this constant will give the needed steps
#Alt - 7000/180 = 38.889
def oneQuickRightTurn(ap1, an1, bp1, bn1, delay):
    CalibrateX(ap1, 0, an1, 1, bp1, 0, bn1, 1)
    time.sleep(delay)
    CalibrateX(ap1, 0, an1, 1, bp1, 1, bn1, 0)
    time.sleep(delay)
    CalibrateX(ap1, 1, an1, 0, bp1, 1, bn1, 0)
    time.sleep(delay)
    CalibrateX(ap1, 1, an1, 0, bp1, 0, bn1, 1)
    time.sleep(delay)
    
def Align(offset, ap1, an1, bp1, bn1, ap2, an2, bp2, bn2):
    #horizontal offset from theta
    #calculate number of horizontal ticks from gear ratio
    xCycles = math.floor(offset[1] * 180 / (math.pi * .1125))
    if xCycles >= 0:
        print('Ticks Right: ' + str(xCycles))
        for ticksRight in range (0, xCycles):
           oneTickRight(ap1, an1, bp1, bn1)
    elif xCycles < 0:
        print('Ticks Left: ' + str(abs(xCycles)))
        for ticksLeft in range (0, abs(xCycles)):
           oneTickLeft(ap1, an1, bp1, bn1)
           
    #vertical offset from phi
    #calculate number of horizontal ticks from gear ratio
    yCycles = math.floor(offset[2] * 180 / (math.pi * .1047))
    if yCycles >= 0:
        print('Ticks Up: ' + str(yCycles))
        for ticksUp in range (0, yCycles):
           oneTickUp(ap2, an2, bp2, bn2)
    elif yCycles < 0:
        print('Ticks Down: ' + str(abs(yCycles)))
        for ticksDown in range (0, abs(yCycles)):
           oneTickDown(ap2, an2, bp2, bn2)
