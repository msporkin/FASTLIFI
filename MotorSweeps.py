#Importing GPIO and time libraries to use sleep and pin functions
import RPi.GPIO as GPIO
import time
import math

#Defining variables
delayC = 2
delay = .0055 #Time delay
xCycles = 0 #Number of positioning steps in the x-direction
yCycles = 0 #Number of positioning steps in the y-direction
z = 6.2 #distance to wall from laser


GPIO.setmode(GPIO.BCM) #Broadcom SOC channel definition of GPIO pins (using designated GPIO pin number versus number on board)
GPIO.setwarnings(False) #Disable warnings - will be cleaned up at the end with cleanup function 

#Defining enable pins on first L298N to GPIOs on Raspberry Pi
ENA1 = 18
ENB1 = 22

#Defining enable pins on second L298N to GPIOs on Raspberry Pi
ENA2 = 25
ENB2 = 16

#Defining winding pins on first L298N to GPIOs on Raspberry Pi
ap1 = 23 #int1
an1 = 24 #int2
bp1 = 4  #int3
bn1 = 17 #int4

#Defining winding pins on second L298N to GPIOs on Raspberry Pi
ap2 = 27
an2 = 13
bp2 = 5
bn2 = 6


#Defining all GPIOs to be output
GPIO.setup(ENA1, GPIO.OUT)
GPIO.setup(ENB1, GPIO.OUT)
GPIO.setup(ap1, GPIO.OUT)
GPIO.setup(an1, GPIO.OUT)
GPIO.setup(bp1, GPIO.OUT)
GPIO.setup(bn1, GPIO.OUT)
GPIO.setup(ENA2, GPIO.OUT)
GPIO.setup(ENB2, GPIO.OUT)
GPIO.setup(ap2, GPIO.OUT)
GPIO.setup(an2, GPIO.OUT)
GPIO.setup(bp2, GPIO.OUT)
GPIO.setup(bn2, GPIO.OUT)

#Defining ENA and ENB to be true/1 to enable A+/A- and B+/B- ports
GPIO.output(ENA1, True)
GPIO.output(ENB1, True)
GPIO.output(ENA2, True)
GPIO.output(ENB2, True)

#Defining calibration for second L298N
def Calibrate1(ap1, state1, an1, state2, bp1, state3, bn1, state4):
    GPIO.output(ap1, state1)
    GPIO.output(an1, state2)
    GPIO.output(bp1, state3)
    GPIO.output(bn1, state4)

#Defining calibration for second L298N
def Calibrate2(ap2, State1, an2, State2, bp2, State3, bn2, State4):
    GPIO.output(ap2, State1)
    GPIO.output(an2, State2)
    GPIO.output(bp2, State3)
    GPIO.output(bn2, State4)

def turnSweep():  #180 degrees in 7000 clicks   
    for cs in range (0,70):
        print(str(cs)+'00')
        for c1 in range (0, 100):
            Calibrate1(ap1, 0, an1, 1, bp1, 0, bn1, 1)
            time.sleep(delay)
            Calibrate1(ap1, 0, an1, 1, bp1, 1, bn1, 0)
            time.sleep(delay)
            Calibrate1(ap1, 1, an1, 0, bp1, 1, bn1, 0)
            time.sleep(delay)
            Calibrate1(ap1, 1, an1, 0, bp1, 0, bn1, 1)
            time.sleep(delay)
        
def tiltSweep():  #45 degrees in 1200 clicks   
    for cs in range (0,12):
        print(str(cs)+'00')
        for c1 in range (0, 100):
            Calibrate2(ap2, 0, an2, 1, bp2, 0, bn2, 1)
            time.sleep(delay)
            Calibrate2(ap2, 0, an2, 1, bp2, 1, bn2, 0)
            time.sleep(delay)
            Calibrate2(ap2, 1, an2, 0, bp2, 1, bn2, 0)
            time.sleep(delay)
            Calibrate2(ap2, 1, an2, 0, bp2, 0, bn2, 1)
            time.sleep(delay)
    for cs in range (0, 26):
        print(str(cs) + '00')
        for c2 in range (0,100):
            Calibrate2(ap2, 1, an2, 0, bp2, 1, bn2, 0)
            time.sleep(delay)
            Calibrate2(ap2, 0, an2, 1, bp2, 1, bn2, 0)
            time.sleep(delay)
            Calibrate2(ap2, 0, an2, 1, bp2, 0, bn2, 1)
            time.sleep(delay) 
            Calibrate2(ap2, 1, an2, 0, bp2, 0, bn2, 1)
            time.sleep(delay)

turnSweep()
tiltSweep()


