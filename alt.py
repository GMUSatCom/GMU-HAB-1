import time
import board
import busio
import adafruit_mpl3115a2
import csv
 
class Alt:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_mpl3115a2.MPL3115A2(self.i2c)
        self.sensor.sealevel_pressure = 102250
 
    def write_data(self):
        # Main loop to read the sensor values and print them every second.
        while True:
            with open('/home/pi/hab/data/alt.csv', 'a') as writeFile:
                writer = csv.writer(writeFile)
                altData = [self.sensor.altitude, self.sensor.temperature, self.sensor.pressure]
                writer.writerow(altData)
                time.sleep(1.0)
