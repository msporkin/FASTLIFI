import RPi.GPIO as GPIO #set up GPIO library
from time import sleep #set up sleep function

GPIO.setmode(GPIO.BCM) #set to use PINs diagram instead of BCM pins
GPIO.setwarnings(False)
GPIO.setup(11,GPIO.OUT) #set PIN 11 as output
GPIO.setup(26,GPIO.OUT) #set PIN 26 as output

ServoX = GPIO.PWM(11,50) #50Hz pulse sent
ServoX.start(0) #start servo at 0

ServoY = GPIO.PWM(26,50) #50Hz pulse sent
ServoY.start(0) #start servo at 0
found = False

test2 = 50
test1 = 31
x,y = 72, 52
Matrix = [[0 for k1 in range(y)] for k2 in range(x)]
Matrix[test2][test1] = 1

found == False

def right(duty1):
    ServoX.ChangeDutyCycle(duty1) #shift in accordance to set duty cycle
    sleep(0.2) #give time to reach position
    ServoX.ChangeDutyCycle(0) #turn off to remove jitter
    sleep(0.2) #give time to reach position
    duty1 = duty1 + 0.1 #100 steps
    return duty1

def down(duty2):
    ServoY.ChangeDutyCycle(duty2) #shift in accordance to set duty cycle
    sleep(0.2) #give time to reach position
    ServoY.ChangeDutyCycle(0) #turn off to remove jitter
    sleep(0.2) #give time to reach position
    duty2 = duty2 + 0.1 #100 steps
    return duty2
    
def left(duty1):
    ServoX.ChangeDutyCycle(duty1) #shift in accordance to set duty cycle
    sleep(0.2) #give time to reach position
    ServoX.ChangeDutyCycle(0) #turn off to remove jitter
    sleep(0.2) #give time to reach position
    duty1 = duty1 - 0.1 #90 steps
    return duty1

def checkPos(a,b,test1,test2):
    global found
    if a == test2 and b == test1:
        found = True
    print('a,b = '+str(a)+','+str(b))

while found == False:
    duty1 = 2 #set servo motor one to 180 degrees (left side)
    duty2 = 2 #set servo motor two to 180 degrees (left side) 
    a=0
    b=0
    
    while duty1 <= 9: #go from 0 to 180 degrees in 100 steps
        if found == False:    
            duty1 = right(duty1)
            a = a+1
            checkPos(a,b,test1,test2)
        else:
            break
    if found == False:
        while duty2 < 4: #go from 0 to 180 degrees in 100 steps
            if found == False:
                duty2 = down(duty2)
                b = b+1
                checkPos(a,b,test1,test2)
            else:
                break
    if found == False:
        while 2.1<= duty1 <= 9.1: #go from 180 to 0 degrees in 100 steps
            if found == False:
                duty1 = left(duty1)
                a = a-1
                checkPos(a,b,test1,test2)
            else:
                break
    if found == False:
        while 4 <= duty2 < 5: #go from 0 to 180 degrees in 100 steps
            if found == False:
                duty2 = down(duty2)
                b = b+1
                checkPos(a,b,test1,test2)
            else:
                break
    if found == False:
        while duty1 <= 9: #go from 0 to 180 degrees in 100 steps
            if found == False:
                duty1 = right(duty1)
                a = a+1
                checkPos(a,b,test1,test2)
            else:
                break
    if found == False:
        while 5 <= duty2 < 7: #go from 0 to 180 degrees in 100 steps
            if found == False:
                duty2 = down(duty2)
                b = b+1
                checkPos(a,b,test1,test2)
            else:
                break
    if found == False:
        while 2.1<= duty1 <= 9.1: #go from 180 to 0 degrees in 100 steps
            if found == False:
                duty1 = left(duty1)
                a = a-1
                checkPos(a,b,test1,test2)
            else:
                break
    if found == False:
        print('Not found, starting over')

print('Found it!')
sleep(2)
#pulse.ChangeDutyCycle(2)
ServoX.stop() #stop running motors
ServoY.stop() #stop running motors
GPIO.cleanup() #cleanup function
