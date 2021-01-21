#Michael Sporkin - Link Communication ADC Subsystem
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
led = LED(21)    #GPIO pin 21 used for LED

# Set up in differential mode between 0 and 1
chan = AnalogIn(ads, ADS.P0, ADS.P1)

with open('test.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter = ',', quotechar='"')
    filewriter.writerow(["Voltage (V)", "Time (sec)"])
    v_sum = 0
    for i in range(0,300):
        filewriter.writerow([chan.voltage,time.process_time()])
        v_sum = v_sum + chan.voltage
        time.sleep(.0015)
    v_avg = round(v_sum/300, 6)
    v_avg_col = []
    for i in range(0,300):
        v_avg_col.append(v_avg)

#Graphing 
with open('test.csv') as csvfile:   
    data = pandas.read_csv('test.csv', delimiter=',')
    data.set_index("Time (sec)", inplace = True)
    data['Average Voltage (V)'] = v_avg_col
    
    data.plot()
    plt.title('Recorded Voltage vs. Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Voltage (V)')
    plt.show()
    
    print('Average Voltage = ' +str(v_avg)+ ' V')
