#Michael Sporkin (with help from Ryan Quinn)
#ECEN 404 - 4 February 2021
#This code controllers the laser diode by toggling a GPIO pin on and off

#Standard Imports
import cv2
import numpy as np
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

laser_pin = 26
GPIO.setup(laser_pin, GPIO.OUT)

toggling = True
while toggling == True:
    laser_status = input()
    if laser_status == 'laser_off':
        GPIO.output(laser_pin, 0)
        print('Laser off. We are safe.')
    elif laser_status == 'laser_on':
        GPIO.output(laser_pin, 1)
        print('Alert: Laser on.')
    elif laser_status == 'q':
        toggling == False
        break

GPIO.cleanup() #wipes GPIO memory for future use
