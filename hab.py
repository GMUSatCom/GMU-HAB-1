import os
from camera import *
from gps import *
from alt import *
import time
import threading

#init the gps object with the file paths and gps serial path
gps = Gps('/home/pi/hab/gpsData/gps.csv', '/dev/ttyS0' )
#Create the altimiter object and initialize it 
alt = Alt('/home/pi/hab/data/alt.csv')
#the current status of the picamera
cam_status = ""

#Target function for the Pycam's thread. Timing is handled by camera.py
#changes the action of the camera based on the altitude of the balloon
def pycam_thread(name):
    while True:
        cam = Camera()
        if gps.get_altitude() > -1.0:
            cam_status = "video"
            cam.takeVideo()
        elif gps.get_altitude() > 10000.0:
            cam_status = "picture"
            cam.takePicture()
        else:
            cam_status = "idle"
        #print(cam_status)
        cam.close()

if __name__ == '__main__':
    
    #create the pycam thread so that it doesn't interfere with DATA collection
    pycam = threading.Thread(target=pycam_thread, args = (1,), daemon=True)
    pycam.start()
    
    #initialize the com port, if it failes handle the failure, possbily exit or dissable the gps
    #to allow the rest of the device to continue to work
    if gps.init_com_port() is False:
        print("Failed to init the com port with the gps module")
    try:
        while True:
            #Call the read every loop to handle the gps data 
            if gps.read() is False:
                # If it failed to read handle? 
                continue    
        
            alt.write_data()
        
            #Remove all unnecessary time delays that can happen from functions called here
            #Use this timer to delay the main thread if other programs can handle it, so
            #things can hopefully be syncronized 
            time.sleep(1.0)
    except KeyboardInterrupt:
        exit(0)
    except:
        pass


