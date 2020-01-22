import adafruit_mpl3115a2
import csv
from os import path

class Alt:
    def __init__(self, file_name, i2c_port):       
        self.i2c_bus = i2c_port
        self.sensor = None        
        self.file_name = file_name
        self.altitude = None
        
    def Begin(self):
        try:
            #The uses the ic2 bus passed in from the objects constructor
            self.sensor = adafruit_mpl3115a2.MPL3115A2(self.i2c_bus)
            self.sensor.sealevel_pressure = 102250
            #If the files dont already exist create new files and add their headers 
            if(path.exists(self.file_name) is False):
                with open(self.file_name, 'w+') as writeFile:
                    writer = csv.DictWriter(writeFile, fieldnames=["Altitude", "Temperature","Pressure"])
                    writer.writeheader()
            return True
        except:
            return False
 
    def update(self):
        try:
            self.altitude = self.sensor.altitude
            alt_data = [self.altitude, self.sensor.temperature, self.sensor.pressure]
            with open(self.file_name, 'a+') as write_file:
                writer = csv.writer(write_file)    
                writer.writerow(alt_data)
            return alt_data
        except:
            return False
            
    def get_altitude(self):
        if self.altitude is None:
            return 0
        try:
            return int(self.altitude)
        except:
            return 0
