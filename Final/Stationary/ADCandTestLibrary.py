#Michael Sporkin - ADCandTestLibrary - 3/8/2021
#Library for all testing/validation based functions, ADC and photodetector

#standard imports
import board
import busio
import csv
import pandas
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

import matplotlib
#matplotlib.use('qt4agg')
import matplotlib.pyplot as plt

i2c = busio.I2C(board.SCL, board.SDA) #allows RPI to communicate with adc
ads = ADS.ADS1115(i2c)
ads.gain = 2/3   #set gain to largest range (+- 6.144)
chan = AnalogIn(ads, ADS.P0, ADS.P1) # Set up in differential mode between 0 and 1

link_threshold = .10 #threshold above which is considered "link establishment"
delayP = .001 #delay for print-style functions

#prints status of beam on photodiode
def printAS(glbl):
    #access global parameters
    while glbl.esc == False:
        #if something changes, write to file
        if glbl.actionString_update != glbl.actionString:
            glbl.setAS(glbl.actionString_update)
            note = '(Time: ' + str(round(time.process_time(),3)) + ' sec) ' + glbl.actionString
            print(note)
        time.sleep(delayP)
    return
   
def pdcGraph(name, glbl, mobPi):
    with open(str(name)+'.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter = ',', quotechar='"')
        filewriter.writerow(["Voltage (V)", "Time (sec)"])
        link_threshold_col = []
        
        while glbl.esc == False:
            if glbl.link == False:
                filewriter.writerow([chan.voltage,time.process_time()])
                link_threshold_col.append(link_threshold)
                time.sleep(delayP)
                #If recorded voltage is larger than the threshold, turn LED on to close loop
                #   and signify alignment
                if chan.voltage > link_threshold:
                    glbl.setASU('Alignment made')
                    glbl.setLink(True)
                    glbl.setMobBlue(False)
                    mobPi.blueToggle(glbl.mobBlue)
                #If just noise, continue searching
                else:
                    glbl.setASU('Ambient Noise. Searching...')
            
            if glbl.link == True:
                filewriter.writerow([chan.voltage,time.process_time()])
                link_threshold_col.append(link_threshold)
                time.sleep(delayP)
                
                if chan.voltage < link_threshold:
                    glbl.setASU('Link lost. Will search with photodiode again.')
                    glbl.setLink(False)
                    glbl.setCalibrated(False)
                    glbl.setStatBlue(False)
                    glbl.setTargetFound(False)
                    glbl.setSweeping(True)
    
    if glbl.esc == True:
        plt.ion()
        data = pandas.read_csv(str(name)+'.csv', delimiter=',')
        data.set_index("Time (sec)", inplace = True)
        data.plot()
        plt.title('Recorded Voltage vs. Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Voltage (V)')
        plt.savefig(str(name)+'.png')
        plt.ioff()
        plt.show()
        return
