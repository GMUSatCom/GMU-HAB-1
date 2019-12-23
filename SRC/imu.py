# Simple demo of the LSM9DS1 accelerometer, magnetometer, gyroscope.
# Will print the acceleration, magnetometer, and gyroscope values every second.
import adafruit_lsm9ds1
import csv

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
            #The uses the current board version i2c pins
            self.sensor = adafruit_lsm9ds1.LSM9DS1_I2C(self.i2c_bus)
            return True
        except:
            return False
        
    def update(self):
        try:
            # Read acceleration, magnetometer, gyroscope, temperature.
            accel_x, accel_y, accel_z = sensor.acceleration
            mag_x, mag_y, mag_z = sensor.magnetic
            gyro_x, gyro_y, gyro_z = sensor.gyro
            temp = sensor.temperature
            imu_data = [accel_x, accel_y, accel_z, mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z, temp]
            with open(self.file_name, 'a') as write_file:
                writer = csv.writer(write_file)
                writer.writerow(imu_data)
            return imu_data
        except:
            return False
        # Print values.
        #print('Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(accel_x, accel_y, accel_z))
        #print('Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(mag_x, mag_y, mag_z))
        #print('Gyroscope (degrees/sec): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(gyro_x, gyro_y, gyro_z))
        #print('Temperature: {0:0.3f}C'.format(temp))
