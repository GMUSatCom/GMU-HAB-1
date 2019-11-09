import time
import board
import busio
import adafruit_mpl3115a2
import csv
 
class Alt:
    def __init__(self, filename):
        #This uses the board program to get the rpi pins for all pins
        #The uses the current board version i2c pins
        self.sensor = adafruit_mpl3115a2.MPL3115A2(busio.I2C(board.SCL, board.SDA))
        self.sensor.sealevel_pressure = 102250
        self.filename = filename
 
    def write_data(self):
        try:
            with open(self.filename, 'a') as writeFile:
                writer = csv.writer(writeFile)
                altData = [self.sensor.altitude, self.sensor.temperature, self.sensor.pressure]
                writer.writerow(altData)                
        
        except KeyboardInterrupt:
            exit(0)
