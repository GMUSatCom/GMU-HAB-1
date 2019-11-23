import adafruit_mpl3115a2
import csv

class Alt:
    def __init__(self, file_name, i2c_port):       
        self.i2c_bus = i2c_port
        self.sensor = None        
        self.file_name = file_name
        self.altitude = None
        
    def Begin(self):
        try:
            #This uses the board program to get the rpi pins for all pins
            #The uses the current board version i2c pins
            self.sensor = adafruit_mpl3115a2.MPL3115A2(self.i2c_bus)
            self.sensor.sealevel_pressure = 102250
            return True
        except:
            return False
 
    def update(self):
        try:
            self.altitude = self.sensor.altitude
            alt_data = [self.altitude, self.sensor.temperature, self.sensor.pressure]
            with open(self.file_name, 'a') as write_file:
                writer = csv.writer(write_file)    
                writer.writerow(alt_data)
            return True
        except:
            return False
            
    def get_altitude(self):
        if self.altitude is None:
            return 0
        try:
            return int(self.altitude)
        except:
            return 0