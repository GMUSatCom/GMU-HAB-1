import os
from camera import *
from gps import *
from alt import *
import time
import threading

#init the gps object with the file paths and gps serial path
gps = Gps('/home/pi/hab/gpsData/gps.csv', '/dev/ttyS0' )
#Create the altimiter object and initialize it 
alt = Alt('/home/pi/hab/altData/alt.csv')
imu = Imu('/home/pi/hab/imuData/imu.csv')
#Target function for the Pycam's thread. Timing is handled by camera.py
#changes the action of the camera based on the altitude of the balloon
def pycam_thread(name):
    #current altitude
    altitude = 0
    #the current status of the picamera
    cam_status = ""
    try:
        while True:
            cam = Camera('/home/pi/hab/vids/','/home/pi/hab/imgs/') # Create the Camera object with the file path
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
            elif gps.get_altitude() > 10000: 
                cam_status = "picture"
                cam.takePicture()
            else:
                cam_status = "idle"
            #print(cam_status)
            cam.close()
    except:
        pass
        
if __name__ == '__main__':
    
    #create the pycam thread so that it doesn't interfere with DATA collection
    #it is a daemon thread, meaning it will close when the main thread exits.
    pycam = threading.Thread(target=pycam_thread, args = (1,), daemon=True)
    pycam.start()
    
    #initialize the com port, if it failes handle the failure, possbily exit or dissable the gps
    #to allow the rest of the device to continue to work
    if gps.init_com_port() is False:
        print("Failed to init the com port with the gps module")
    try:
        while True:
            #Write Altimeter data
            alt.update()
            #Call the read every loop to handle the gps data 
            if gps.update() is False:
                # If it failed to read handle? 
                continue    
        
            
        
            #Remove all unnecessary time delays that can happen from functions called here
            #Use this timer to delay the main thread if other programs can handle it, so
            #things can hopefully be syncronized 
            time.sleep(1.0)
    except KeyboardInterrupt:
        exit(0)
    except:
        pass