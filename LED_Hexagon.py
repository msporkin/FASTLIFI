import numpy as np
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

BlueLED = 21
Hexa = 20

GPIO.setup(BlueLED, GPIO.OUT)
GPIO.setup(Hexa, GPIO.OUT)

toggling = True
while toggling == True:
    user_input = input()
    if user_input == 'Hexagon':
        GPIO.output(Hexa, 1)
    elif user_input == 'Blue LED':
        GPIO.output(BlueLED, 1)
    elif user_input == 'Both':
        GPIO.output(Hexa, 0)
        GPIO.output(BlueLED, 0)
    elif user_input == 'Q':
        toggling == False
        break
    