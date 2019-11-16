import pynmea2
import serial
import time
import csv

# Reads GPS Data and writes it to gps.csv
# B I G         B R A I N          T I M E
class Gps:
    def __init__(self, filename, com_port):
        self.com_location = com_port
        self.com = None
        self.filename = filename
        self.connected = False
        self.altitude = None
        
    def init_com_port(self):
         #attempt to init the com port for the gps serial connection   
        try:
            #assign the serial port using the filename var (com port object)
            self.com = serial.Serial(self.com_location, timeout=5.0)
            #were connected so the rest of the code can execute
            self.connected = True
            #return 
            return True
        #can't connect on serial com
        except serial.SerialException:            
            return False

    def read(self):              
        
        if self.connected is False:
            return False
        
        try:
            location = pynmea2.parse(self.com.readline().decode("utf-8")) # parse into an object with gps data            
            self.altitude = location.altitude
            gpsData = [location.latitude, location.longitude, location.altitude, location.num_sats, location.timestamp, location.horizontal_dil]
            # put gps data in an array
            # open a writer using the csv library
            with open(self.filename, 'a') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow(gpsData)
            
            #print the values
            #print("DEBUG for gps data")
            #for i in range(len(gpsData)):
            #    print(gpsData[i])                
            #    print(", ")             
            #everything worked return true
            return True
            
        #failed while hanleing gps coms return false    
        except:
            return False            

    def get_altitude(self):
        if self.altitude is None:
            return 0
        try:
            return int(self.altitude)
        except:
            return 0