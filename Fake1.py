#Clockwise motion/Rotating and Tilting Platform Program

#Importing GPIO and time libraries to use sleep and pin functions
import RPi.GPIO as GPIO
import time

#Defining variables
ThreeCycles = 1 #Amount of times to run 4 cycles (7.2 degrees) due to stepper windings
delay = 1 #Time delay in ms

GPIO.setmode(GPIO.BCM) #Broadcom SOC channel definition of GPIO pins (using designated GPIO pin number versus number on board)
GPIO.setwarnings(False) #Disable warnings - will be cleaned up at the end with cleanup function 

#Defining enable pins on L298N to GPIOs on Raspberry Pi
ENA = 18
ENB = 22

#Defining winding pins on L298N to GPIOs on Raspberry Pi
INT1isAp = 23
INT2isAn = 24
INT3isBp = 4
INT4isBn = 17

#Defining all GPIOs to be output
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(INT1isAp, GPIO.OUT)
GPIO.setup(INT2isAn, GPIO.OUT)
GPIO.setup(INT3isBp, GPIO.OUT)
GPIO.setup(INT4isBn, GPIO.OUT)

#Defining ENA and ENB to be true/1 to enable A+/A- and B+/B- ports
GPIO.output(ENA, True)
GPIO.output(ENB, True)

#Defining one cycle (1.8 degree step) 
def OneCycle(State1, State2, State3, State4):
  GPIO.output(INT1isAp, State1)
  GPIO.output(INT2isAn, State2)
  GPIO.output(INT3isBp, State3)
  GPIO.output(INT4isBn, State4)

#Calibration sequence to allow gears to catch on platform
OneCycle(1,0,1,0)
time.sleep(1)
print("Calibrate 1")
OneCycle(0,1,1,0)
time.sleep(1)
print("Calibrate 2")
OneCycle(0,1,0,1)
time.sleep(1)
print("Calibrate 3")
OneCycle(1,0,0,1)
time.sleep(1)
print("Calibrate 4")
OneCycle(1,0,1,0)
time.sleep(1)
print("Calibrate 5")
OneCycle(0,1,1,0)
time.sleep(1)
print("Calibrate 6")
OneCycle(0,1,0,1)
time.sleep(1)
print("Calibrate 7")
OneCycle(1,0,0,1)
time.sleep(1)
print("Calibrate 8")


color = input("Enter a color: ");
if color in ['g', 'green']:
    time.sleep(1000)
else:
    OneCycle(1,0,1,0)
    time.sleep(1)
    print("Step 1")
    
color = input("Enter a color: ");
if color in ['g', 'green']:
    time.sleep(1000)
else:
    OneCycle(0,1,1,0)
    time.sleep(1)
    print("Step 2")
    
color = input("Enter a color: ");
if color in ['g', 'green']:
    time.sleep(1000)
else:
    OneCycle(0,1,0,1)
    time.sleep(1)
    print("Step 3")
    
color = input("Enter a color: ");
if color in ['g', 'green']:
    time.sleep(1000)
else:
    OneCycle(1,0,0,1)
    time.sleep(1)
    print("Step 4")

if OneCycle(1,0,1,0):
    OneCycle(0,1,1,0)

 

