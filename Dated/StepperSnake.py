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

def Left():
    Calibrate1(0,1,0,1)
    time.sleep(delay)
    Calibrate1(0,1,1,0)
    time.sleep(delay)
    Calibrate1(1,0,1,0)
    time.sleep(delay)
    Calibrate1(1,0,0,1)
    time.sleep(delay)
    print("Left!")
    
def Right():
    Calibrate1(1,0,1,0)
    time.sleep(delay)
    Calibrate1(0,1,1,0)
    time.sleep(delay)
    Calibrate1(0,1,0,1)
    time.sleep(delay)
    Calibrate1(1,0,0,1)
    time.sleep(delay)
    print("Right!")
    
def Down():
    Calibrate2(0,1,0,1)
    time.sleep(delay)
    Calibrate2(0,1,1,0)
    time.sleep(delay)
    Calibrate2(1,0,1,0)
    time.sleep(delay)
    Calibrate2(1,0,0,1)
    time.sleep(delay)
    print("Down!")
    
def Up():
    Calibrate2(1,0,1,0)
    time.sleep(delay)
    Calibrate2(0,1,1,0)
    time.sleep(delay)
    Calibrate2(0,1,0,1)
    time.sleep(delay)
    Calibrate2(1,0,0,1)
    time.sleep(delay)
    print("Up!")
"""
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
"""

test2 = 19
test1 = 1
x,y = 1000, 10
Matrix = [[0 for k1 in range(y)] for k2 in range(x)]
Matrix[test2][test1] = 1

q1 = 0
q2 = 0
f1 = 0
found = False
if found == False:
    while q1 < y and found == False:
        while q2 < x and found == False:
            print("q2, q1 =  " +str(q2) + " " + str(q1))
            if q1 == test1 and q2 == test2:
                print("Found point!")
                found = True
                break
            elif q1 % 2 == 0:
                Right()
                if q2 == x-1:
                    break
                q2 = q2 + 1
            else:
                Left()
                if q2 == 0:
                    break
                q2 = q2 - 1
        if found == True:
            break
        Up()
        q1 = q1 + 1
print("Done Snake!")
