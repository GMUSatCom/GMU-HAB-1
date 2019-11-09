import os
from camera import *
from gps import *
from alt import *

print("boi")
cam = Camera()
#init the gps object with the file paths and gps serial path
gps = Gps('/home/pi/hab/gpsData/gps.csv', '/dev/ttyS0' )
#Create the altimiter object and initialize it 
alt = Alt('/home/pi/hab/data/alt.csv')

#initialize the com port, if it failes handle the failure, possbily exit or dissable the gps
#to allow the rest of the device to continue to work
if gps.init_com_port() is False:
    print("Failed to init the com port with the gps module")

while True:
    #Call the read every loop to handle the gps data 
    if gps.read() is False:
        # If it failed to read handle? 
        continue
        
    alt.write_data()    
    
    
    #cam.takePicture()
    #cam.takePicture()
    #cam.takeVideo()

    #cam.close()
    
    #Remove all unnecessary time delays that can happen from functions called here
    #Use this timer to delay the main thread if other programs can handle it, so
    #things can hopefully be syncronized 
    time.sleep(1.0)
    

