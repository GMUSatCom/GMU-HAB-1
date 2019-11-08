import pynmea2
import serial
import time
import csv

# Reads GPS Data and writes it to gps.csv
# B I G         B R A I N          T I M E
class Gps: 
    def read_serial(self, filename):
        com = None
        while True:
            # Big brain GPS data extraction
            if com is None:
              try:
                com = serial.Serial(filename, timeout=5.0)
              except serial.SerialException:
                print('could not connect to %s' % filename)
                time.sleep(5.0)
                continue
            
            try:
                data = com.readline() #read from com
                location = pynmea2.parse(data) # parse into an object with gps data
                gpsData = [location.latitude, location.longitude, location.altitude, location.num_sats, location.timestamp, location.horizontal_dil]
                            # put gps data in an array
                
                #open a writer using the csv library
                with open('/home/pi/hab/data/gps.csv', 'a') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerow(gpsData)
                
                #print the values
                for i in range(len(gpsData)):
                    print(gpsData[i])
                    print(", ")
                    
            #exit if you press cntrl + c
            except KeyboardInterrupt:
                exit(0)
                
            except:
                pass
            
#calls the function
# read_serial('/dev/ttyS0')
