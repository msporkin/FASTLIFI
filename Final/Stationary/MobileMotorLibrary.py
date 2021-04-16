#Michael Sporkin - Mobile Motor support library for mobile-module-specific functions
import RPi.GPIO as GPIO
import time
import math

#Broadcom channel definition of GPIO pins (using designated GPIO pin number)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) #Disable warnings

#Set motor variables
delayXY = .2 #Time delay - servo motors

class MobPi:
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
        
        #Define servo motor pins
        self.servoGPIOX = 11
        self.servoGPIOY = 26
        
        self.blueLed = 21
        self.hexagon = 20

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
        GPIO.setup(self.servoGPIOX, GPIO.OUT) 
        GPIO.setup(self.servoGPIOY, GPIO.OUT)
        GPIO.setup(self.blueLed, GPIO.OUT)
        GPIO.setup(self.hexagon, GPIO.OUT)
        
        GPIO.output(self.hexagon, True)

        #Defining ENA and ENB to be true/1 to enable A+/A- and B+/B- ports
        GPIO.output(self.ENA1, True)
        GPIO.output(self.ENB1, True)
        GPIO.output(self.ENA2, True)
        GPIO.output(self.ENB2, True)
        
        self.servoX = GPIO.PWM(self.servoGPIOX,50) #50Hz pulse sent
        self.servoX.start(0) #start servo at 0
        self.servoY = GPIO.PWM(self.servoGPIOY,50) #50Hz pulse sent
        self.servoY.start(0) #start servo at 0
    
    def blueToggle(self, blue):
        GPIO.output(self.blueLed, blue)

#####################################
######### SERVO FUNCTIONS ###########
#####################################

def rightServo(duty1, ServoX):
    ServoX.ChangeDutyCycle(duty1) #shift in accordance to set duty cycle
    time.sleep(delayXY) #give time to reach position
    ServoX.ChangeDutyCycle(0) #turn off to remove jitter
    time.sleep(delayXY) #give time to reach position
    duty1 = duty1 + 0.1 #100 steps
    return duty1

def downServo(duty2, ServoY):
    ServoY.ChangeDutyCycle(duty2) #shift in accordance to set duty cycle
    time.sleep(delayXY) #give time to reach position
    ServoY.ChangeDutyCycle(0) #turn off to remove jitter
    time.sleep(delayXY) #give time to reach position
    duty2 = duty2 + 0.1 #100 steps
    return duty2
    
def leftServo(duty1, ServoX):
    ServoX.ChangeDutyCycle(duty1) #shift in accordance to set duty cycle
    time.sleep(delayXY) #give time to reach position
    ServoX.ChangeDutyCycle(0) #turn off to remove jitter
    time.sleep(delayXY) #give time to reach position
    duty1 = duty1 - 0.1 #90 steps
    return duty1

def upServo(duty2, ServoY):
    ServoY.ChangeDutyCycle(duty2) #shift in accordance to set duty cycle
    time.sleep(delayXY) #give time to reach position
    ServoY.ChangeDutyCycle(0) #turn off to remove jitter
    time.sleep(delayXY) #give time to reach position
    duty2 = duty2 - 0.1 #100 steps
    return duty2

#AlignmentTest starts with the photodetector centered, then moves approx. 1 inch
#right, left, down, and up from center to see where it crosses a peak threshold
def alignmentTestServo(servoX, servoY, glbl):
    print('Beginning XY alignment')
    #Centered duty cycle
    duty1 = 5.5
    duty2 = 5.5

    while duty1 < 8.5 and glbl.link == False and glbl.esc == False:
        duty1 = rightServo(duty1, servoX)
    while duty1 > 2.5 and glbl.link == False and glbl.esc == False:
        duty1 = leftServo(duty1, servoX)
    while duty1 <= 6 and glbl.link == False and glbl.esc == False:
        duty1 = rightServo(duty1, servoX)
    while duty2 < 8.5 and glbl.link == False and glbl.esc == False:
        duty2 = downServo(duty2, servoY)
    while duty2 > 2.5 and glbl.link == False and glbl.esc == False:
        duty2 = upServo(duty2, servoY)
    while duty2 <= 5.5 and glbl.link == False and glbl.esc == False:
        duty2 = downServo(duty2, servoY)
    
    if glbl.link == False:
        print('VCSEL not found.')
        glbl.setEsc(True)
    else:
        print('Representative link established')
        glbl.setMobBlue(True)
        
def servoSnake(servoX, servoY, glbl):
    duty1 = 2 #set servo motor one to 180 degrees (left side)
    duty2 = 2 #set servo motor two to 180 degrees (left side)
    #bring PD to origin in bottom right corner
    for i in range(5):
        duty1 = rightServo(2, servoX)
    for j in range(5):
        duty2 = downServo(2, servoY)
    
    print('Beginning XY alignment')
    while glbl.link == False and glbl.esc == False:
        
        while duty1 <= 9 and glbl.link == False: #go from 0 to 180 degrees in 100 steps   
            duty1 = rightServo(duty1, servoX)
        while duty2 < 3 and glbl.link == False: #go from 0 to 180 degrees in 100 steps
            duty2 = downServo(duty2, servoY)
        while 2.1<= duty1 <= 9.1 and glbl.link == False: #go from 180 to 0 degrees in 100 steps
            duty1 = leftServo(duty1, servoX)
        while 3 <= duty2 < 4 and glbl.link == False: #go from 0 to 180 degrees in 100 steps
            duty2 = downServo(duty2, servoY)
        while duty1 <= 9 and glbl.link == False: #go from 0 to 180 degrees in 100 steps
            duty1 = rightServo(duty1, servoX)
        while 4 <= duty2 < 5 and glbl.link == False: #go from 0 to 180 degrees in 100 steps
            duty2 = downServo(duty2, servoY)
        while 2.1<= duty1 <= 9.1 and glbl.link == False: #go from 180 to 0 degrees in 100 steps
            duty1 = leftServo(duty1, servoX)
        while 5 <= duty2 < 6 and glbl.link == False: #go from 0 to 180 degrees in 100 steps
            duty2 = downServo(duty2, servoY)    
        while duty1 <= 9 and glbl.link == False: #go from 0 to 180 degrees in 100 steps
            duty1 = rightServo(duty1, servoX)
        while 6 <= duty2 < 7 and glbl.link == False: #go from 0 to 180 degrees in 100 steps
            duty2 = downServo(duty2, servoY)
        while 2.1<= duty1 <= 9.1 and glbl.link == False: #go from 180 to 0 degrees in 100 steps
            duty1 = leftServo(duty1, servoX)
        while 7 <= duty2 < 8 and glbl.link == False: #go from 0 to 180 degrees in 100 steps
            duty2 = downServo(duty2, servoY)
        while 2.1<= duty1 <= 9.1 and glbl.link == False: #go from 180 to 0 degrees in 100 steps
            duty1 = leftServo(duty1, servoX)
        while 8 <= duty2 < 9 and glbl.link == False: #go from 0 to 180 degrees in 100 steps
            duty2 = downServo(duty2, servoY)
        while duty1 <= 9 and glbl.link == False: #go from 0 to 180 degrees in 100 steps
            duty1 = rightServo(duty1, servoX)
        
        if glbl.link == False:
            print('ERROR: Expected beam not found within XY axis area.')
            glbl.setEsc(True)
    
    if glbl.link == True:    
        print('Representative link established')
        
    if glbl.esc == True:
        servoX.stop()
        servoY.stop()
