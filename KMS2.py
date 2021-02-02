#Importing GPIO and time libraries to use sleep and pin functions
import RPi.GPIO as GPIO
import time
import math

#Defining variables
delay = 1 #Time delay in ms
xCycles = 0 #Number of positioning steps in the x-direction
yCycles = 0 #Number of positioning steps in the y-direction


GPIO.setmode(GPIO.BCM) #Broadcom SOC channel definition of GPIO pins (using designated GPIO pin number versus number on board)
GPIO.setwarnings(False) #Disable warnings - will be cleaned up at the end with cleanup function 

#Defining enable pins on first L298N to GPIOs on Raspberry Pi
ENA1 = 18
ENB1 = 22

#Defining enable pins on second L298N to GPIOs on Raspberry Pi
ENA2 = 25
ENB2 = 16

#Defining winding pins on first L298N to GPIOs on Raspberry Pi
INT1isAp1 = 23
INT2isAn1 = 24
INT3isBp1 = 4
INT4isBn1 = 17

#Defining winding pins on second L298N to GPIOs on Raspberry Pi
INT1isAp2 = 27
INT2isAn2 = 13
INT3isBp2 = 5
INT4isBn2 = 6


#Defining all GPIOs to be output
GPIO.setup(ENA1, GPIO.OUT)
GPIO.setup(ENB1, GPIO.OUT)
GPIO.setup(INT1isAp1, GPIO.OUT)
GPIO.setup(INT2isAn1, GPIO.OUT)
GPIO.setup(INT3isBp1, GPIO.OUT)
GPIO.setup(INT4isBn1, GPIO.OUT)
GPIO.setup(ENA2, GPIO.OUT)
GPIO.setup(ENB2, GPIO.OUT)
GPIO.setup(INT1isAp2, GPIO.OUT)
GPIO.setup(INT2isAn2, GPIO.OUT)
GPIO.setup(INT3isBp2, GPIO.OUT)
GPIO.setup(INT4isBn2, GPIO.OUT)

#Defining ENA and ENB to be true/1 to enable A+/A- and B+/B- ports
GPIO.output(ENA1, True)
GPIO.output(ENB1, True)
GPIO.output(ENA2, True)
GPIO.output(ENB2, True)

#Defining calibration for first L298N
winding_i1 = 0
winding_j1 = 0
def Calibrate1(State1, State2, State3, State4):
    GPIO.output(INT1isAp1, State1)
    GPIO.output(INT2isAn1, State2)
    GPIO.output(INT3isBp1, State3)
    GPIO.output(INT4isBn1, State4)
    global winding_i1
    winding_i1 = 0
    global winding_j1
    winding_j1 = 0
    
#Defining calibration for second L298N
winding_i2 = 0
winding_j2 = 0
def Calibrate2(State1, State2, State3, State4):
    GPIO.output(INT1isAp2, State1)
    GPIO.output(INT2isAn2, State2)
    GPIO.output(INT3isBp2, State3)
    GPIO.output(INT4isBn2, State4)
    global winding_i2
    winding_i2 = 0
    global winding_j2
    winding_j2 = 0
    
#Defining one cycle in clockwise direction(1.8 degree step) for first L298N
def OneCycleClk1():
    global winding_i1
    if winding_i1 > 3:
        winding_i1 = 0 
    if winding_i1 == 0:
          GPIO.output(INT1isAp1, 1)
          GPIO.output(INT2isAn1, 0)
          GPIO.output(INT3isBp1, 1)
          GPIO.output(INT4isBn1, 0)
          time.sleep(delay)
    if winding_i1 == 1:      
          GPIO.output(INT1isAp1, 0)
          GPIO.output(INT2isAn1, 1)
          GPIO.output(INT3isBp1, 1)
          GPIO.output(INT4isBn1, 0)
          time.sleep(delay)
    if winding_i1 == 2:      
          GPIO.output(INT1isAp1, 0)
          GPIO.output(INT2isAn1, 1)
          GPIO.output(INT3isBp1, 0)
          GPIO.output(INT4isBn1, 1)
          time.sleep(delay)
    if winding_i1 == 3:      
          GPIO.output(INT1isAp1, 1)
          GPIO.output(INT2isAn1, 0)
          GPIO.output(INT3isBp1, 0)
          GPIO.output(INT4isBn1, 1)
          time.sleep(delay)
    winding_i1 = winding_i1 + 1
    
#Defining one cycle in clockwise direction(1.8 degree step) for second L298N
def OneCycleClk2():
    global winding_i2
    if winding_i2 > 3:
        winding_i2 = 0 
    if winding_i2 == 0:
          GPIO.output(INT1isAp2, 1)
          GPIO.output(INT2isAn2, 0)
          GPIO.output(INT3isBp2, 1)
          GPIO.output(INT4isBn2, 0)
          time.sleep(delay)
    if winding_i2 == 1:      
          GPIO.output(INT1isAp2, 0)
          GPIO.output(INT2isAn2, 1)
          GPIO.output(INT3isBp2, 1)
          GPIO.output(INT4isBn2, 0)
          time.sleep(delay)
    if winding_i2 == 2:      
          GPIO.output(INT1isAp2, 0)
          GPIO.output(INT2isAn2, 1)
          GPIO.output(INT3isBp2, 0)
          GPIO.output(INT4isBn2, 1)
          time.sleep(delay)
    if winding_i2 == 3:      
          GPIO.output(INT1isAp2, 1)
          GPIO.output(INT2isAn2, 0)
          GPIO.output(INT3isBp2, 0)
          GPIO.output(INT4isBn2, 1)
          time.sleep(delay)
    winding_i2 = winding_i2 + 1

for r1 in range (0,10):
    Calibrate1(1,0,1,0)
    time.sleep(delay)
    Calibrate1(0,1,1,0)
    time.sleep(delay)
    Calibrate1(0,1,0,1)
    time.sleep(delay)
    Calibrate1(1,0,0,1)
    time.sleep(delay)
print("ClockwiseR calibration check!")
time.sleep(5)

color = 0
size = 0
while size != 1 or color != 1:
    color = input("What is the color: ")
    color = float(color)
    size = input("What is the size: ")
    size = float(size)
    if size != 1 or color != 1:
        OneCycleClk1()
print("Saw green hexagon!")



