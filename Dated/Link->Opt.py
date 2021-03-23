#Michael Sporkin - Link Communication ADC integration with Optical Subsystem

#standard imports
import time
import board
import busio
import csv
import threading
import pandas
import matplotlib.pyplot as plt
from gpiozero import LED

# import adafruit_ads1x15.ads1015 as ADS
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
#allows RPI to communicate with adc
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

ads.gain = 2/3   #set gain to largest range (+- 6.144)
searching = True #global searching parameter

#arbitrary thresholds - to be determined by research
distance_threshold = 1.00
noise_threshold = .050

def escape():
    global searching   #access global parameter
    while searching == True:
        if input() == 'q': #any input will turn searching false
            searching = False
    return

def printAS():
    #access global parameters
    global searching
    global actionString
    global actionString_update
    
    with open('logChanges.txt', 'w') as txtfile:
        while searching == True:
            #if something changes, write to file
            if actionString_update != actionString:
                actionString = actionString_update
                note = '(Time: ' + str(round(time.process_time(),3)) + ' sec) ' + actionString
                print(note)
                txtfile.write(note + '\n')
            time.sleep(.0005)
    return

#escape sits idle waiting for input in background
threading.Thread(target=escape).start()

#prints the current state every 1 second
actionString = ''
actionString_update = 'Starting...'
threading.Thread(target=printAS).start()

# Set up in differential mode between 0 and 1
chan = AnalogIn(ads, ADS.P0, ADS.P1)

with open('test.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter = ',', quotechar='"')
    filewriter.writerow(["Voltage (V)", "Time (sec)"])
    noise_threshold_col = []
    distance_threshold_col = []
    while searching:
        #If recorded voltage is larger than the threshold, turn LED on to close loop
        #   and signify alignment
        if chan.voltage > distance_threshold:
            actionString_update = 'Alignment made'
            led.on()
        #If recorded voltage less than threshold but greater than noise, send position
        #   to motors for further instruction
        elif chan.voltage > noise_threshold:
            actionString_update = 'Imperfect Alignment. Motor adjustments needed.'
            led.off()
        #If neither (just room noise), continue searching
        else:
            actionString_update = 'Ambient Noise. Stil searching...'
            led.off()
        
        filewriter.writerow([chan.voltage,time.process_time()])
        noise_threshold_col.append(noise_threshold)
        distance_threshold_col.append(distance_threshold)
        time.sleep(.0015)

#Graphing 
with open('test.csv') as csvfile:   
    data = pandas.read_csv('test.csv', delimiter=',')
    data.set_index("Time (sec)", inplace = True)
    data['Noise Threshold'] = noise_threshold_col
    data['Distance Threshold'] = distance_threshold_col
    
    data.plot()
    plt.title('Recorded Voltage vs. Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Voltage (V)')
    plt.show()
