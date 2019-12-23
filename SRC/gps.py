import pynmea2
import serial
import csv

# Reads GPS Data and writes it to gps.csv
# B I G         B R A I N          T I M E
class Gps:
    def __init__(self, file_name, com_port):
        self.com_location = com_port
        self.com = None
        self.file_name = file_name
        self.connected = False
        self.altitude = None
        
    def Begin(self):
         #attempt to init the com port for the gps serial connection   
        try:
            #assign the serial port using the filename var (com port object)
            self.com = serial.Serial(self.com_location, timeout=5.0)
            #were connected so the rest of the code can execute
            self.connected = True
            #return 
            return True
        #can't connect on serial com
        except:            
            return False

    def update(self):
        
        if self.connected is False:
            return False
        
        try:
            location = pynmea2.parse(self.com.readline().decode("utf-8")) # parse into an object with gps data            
            self.altitude = location.altitude
            gpsData = [location.latitude, location.longitude, location.altitude, location.num_sats, location.timestamp, location.horizontal_dil]
            # put gps data in an array
            # open a writer using the csv library
            with open(self.file_name, 'a') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow(gpsData)            
            
            return gpsData
            
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
