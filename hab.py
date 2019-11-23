import os
import time
import threading
import board
import busio
from camera import *
from gps import *
from alt import *
from imu import *

#TODO:
#Handle I/O errors
#run hab.py on startup

sleep_delay = 1.0
#Primary ic bus
i2c_port = busio.I2C(board.SCL, board.SDA)

#init the gps object with the file paths and gps serial path
gps = Gps('/home/pi/hab/gpsData/gps.csv', '/dev/ttyS0' )
#Create the altimiter object and initialize it 
alt = Alt('/home/pi/hab/altData/alt.csv', i2c_port)
#IMU object
imu = Imu('/home/pi/hab/imuData/imu.csv', i2c_port)
# Create the Camera object with the file path
cam = Camera('/home/pi/hab/vids/','/home/pi/hab/imgs/') 
#Target function for the Pycam's thread. Timing is handled by camera.py
#changes the action of the camera based on the altitude of the balloon


def pycam_thread(name):
    #current altitude
    altitude = 0
    #the current status of the picamera
    cam_status = ""
    try:
        while True:            
            success = 0 # Counts the successful calls to get altitude
            temp_altitude = altitude #temporary storage for altitude
            altitude = 0
            
            #Averages both GPS and Altimeter Altitude readings (If they updated correctly)
            if gps.get_altitude() != 0: # Has not errored
                altitude += gps.get_altitude()
                success += 1
            if alt.get_altitude() != 0: # Has not errored
                altitude += alt.get_altitude()
                success += 1
            if success != 0:
                altitude /= success
            else:
                altitude = temp_altitude            
            
            if gps.get_altitude() > 0:
                cam_status = "video"
                cam.takeVideo()
            elif gps.get_altitude() > 4000: 
                cam_status = "picture"
                cam.takePicture()
            else:
                cam_status = "idle"
            #print(cam_status)
            cam.close()
    except:
        pass
        
if __name__ == '__main__':
    try:
        print("Starting")
        #initialize the com port, its status belongs to the gps active var
        gps_active = gps.Begin()
        # init the imu port
        imu_active = imu.Begin()
        #init the altimiter
        alt_active = atl.Begin()
        
        if gps_active == False:
            print("gps not active")
        if imu_active == False:
            print("imu not active")
        if alt_active == False:
            print("alt not active")
            
        #the pycam thread so that it doesn't interfere with DATA collection
        #it is a daemon thread, meaning it will close when the main thread exits.
        pycam = threading.Thread(target=pycam_thread, args = (1,), daemon=True)
        pycam.start()
        
        while True:
            
            
            #Write Altimeter data only if it was started successfully
            if alt_active is True:
                if alt.update() is False:           
                    #Gps failed to update handle
                    print("Alt failed to update")
                    pass
                
            #If the gps is successfully started then use it skip it
            if gps_active is True:
                if gps.update() is False:
                    # If it failed to read the gps
                    print("gps failed to update")
                    pass
                
            if imu_active is True:
                if imu.update() is False:
                    #handle exception
                    print("Imu failed to update")
                    pass
                    
            #all unnecessary time delays that can happen from functions called here
            #Use this timer to delay the main thread if other programs can handle it, so
            #things can hopefully be syncronized 
            time.sleep(sleep_delay)
    except KeyboardInterrupt:
        exit(0)
    except:
        pass