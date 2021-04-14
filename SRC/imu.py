# Simple demo of the LSM9DS1 accelerometer, magnetometer, gyroscope.
# Will print the acceleration, magnetometer, and gyroscope values every second.
import adafruit_lsm9ds1
import csv
from os import path

class Imu:
    def __init__(self, file_name, i2c_port):  
        # I2C connection:
        self.sensor = None
        self.i2c_bus = i2c_port
        self.file_name = file_name
        # loop will read the acceleration, magnetometer, gyroscope, Temperature
        # values every second and print them out.        
        
    def Begin(self):
        try:
            #This uses the board program to get the rpi pins for all pins
            #The uses the ic2 bus passed in from the objects constructor
            self.sensor = adafruit_lsm9ds1.LSM9DS1_I2C(self.i2c_bus)
            #If the files dont already exist create new files and add their headers 
            if(path.exists(self.file_name) is False):
                with open(self.file_name, 'w+') as writeFile:
                    writer = csv.DictWriter(writeFile, fieldnames=["accel_x", "accel_y", "accel_z", "mag_x", "mag_y", "mag_z", "gyro_x", "gyro_y", "gyro_z", "temp"])
                    writer.writeheader()
            return True
        except:
            return False
        
    def update(self):
        try:
            # Read acceleration, magnetometer, gyroscope, temperature.
            accel_x, accel_y, accel_z = self.sensor.acceleration
            mag_x, mag_y, mag_z = self.sensor.magnetic
            gyro_x, gyro_y, gyro_z = self.sensor.gyro
            temp = self.sensor.temperature
            imu_data = [accel_x, accel_y, accel_z, mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z, temp]
            with open(self.file_name, 'a+') as write_file:
                writer = csv.writer(write_file)
                writer.writerow(imu_data)
            #just return the imu acceleration, and the measured outside temp. 
            return str(accel_x) + ", "+ str(accel_y) +", "+ str(accel_z) +","+ str(temp)
        except:
            return False
