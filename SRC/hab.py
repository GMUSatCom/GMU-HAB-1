import os
import time
import threading
import busio
from board import *
from camera import *
from gps import *
from alt import *
from imu import *
from radio import *
from os import *

#TODO:
#run hab.py on startup

#Primary ic bus
i2c_port = busio.I2C(SCL, SDA)
#install root path 
root_dir = path.dirname(path.realpath(__file__))
csv_dir = root_dir+'/data'
print("Working directory: "+root_dir)
print("Captured data directory: "+csv_dir)
#Create the gps object with the file paths and gps serial path
gps = Gps(csv_dir+'/gps.csv', '/dev/ttyS0' )
#gps lock object for syncronized access
gps_lock = threading.Lock()
#Create the altimiter object and initialize it 
alt = Alt(csv_dir+'/alt.csv', i2c_port)
#altimeter lock object for syncronized access
alt_lock = threading.Lock()
#IMU object
imu = Imu(csv_dir+'/imu.csv', i2c_port)
# Create the Camera object with the file path
cam = Camera(csv_dir+'/vids/',csv_dir+'/imgs/')
#Radio Data tags (must match groundstation software!)  
imu_data_tag = bytes(b'\x02')
gps_data_tag = bytes(b'\x03')
alt_data_tag = bytes(b'\x04')
beacon_tag=bytes(b'\xFF')
#Radio Header IDs (Must match receiver firmware!) 
radio_id = bytes(b'\x0A')
gs_id = bytes(b'\x0A')
#Radio Stream Object. Allows for writing to the radio data stream listener
radio = RadioStream('/dev/lorastream.bin', radio_id , gs_id )

if(path.exists(csv_dir) is False):
    try:
        os.mkdir(csv_dir)
        os.mkdir(csv_dir+'/vids/')
        os.mkdir(csv_dir+'/imgs/')
        
    except:
        print("Could not make directories, exiting")
        exit(0)
#Target function for the Pycam's thread. Timing is handled by camera.py
#changes the action of the camera based on the altitude of the balloon
def pycam_thread(name):
        #current altitude
        altitude = 0
        #the current status of the picamera
        cam_status = "idle"
        try:
                while True: 
			#counts the successful calls to get altitude
                        success = 0 
                        #averages both GPS and Altimeter Altitude readings (If they updated correctly)
                        altitude = 0
                        
                        #Attempt to acqurie a lock on the gps lock object and block the thread until we acquire it
                        with gps_lock:
                                alt_1 = gps.get_altitude()                       
                        
                        if gps_alt != 0: # Has not errored
                                altitude += gps_alt
                                success += 1
                        #Attempt to acqurie a lock on the altimeter lock object and block the thread until we acquire it
                        with alt_lock:
                                alt_2 = alt.get_altitude()
               
                        if alt_2 != 0: # Has not errored
                                altitude += alt_2
                                success += 1

                        if success != 0:
                                altitude /= success
                                if altitude > 0 and altitude < 30000:
                                        cam_status = "video"
                                        cam.takeVideo()
                                elif altitude > 30000: 
                                        cam_status = "picture"
                                        cam.takePicture()
                                else:
                                        cam_status = "idle"
        except:
               pass

if __name__ == '__main__':
    try:
        print("Starting")
        #initialize the com port, its status belongs to the gps active var
        gps_active = gps.Begin()
        #init the imu port
        imu_active = imu.Begin()
        #init the altimiter
        alt_active = alt.Begin()

        if gps_active == False:
            print("Could not start gps module, running without it!")
            radio.Send(gps_data_tag, "Disabled")
        if imu_active == False:
            print("Could not start imu module, running without it!")
            radio.Send(imu_data_tag, "Disabled")
        if alt_active == False:
            print("Could not start altimeter module, running without it!")
            radio.Send(alt_data_tag, "Disabled")

        #the pycam thread so that it doesn't interfere with DATA collection
        #it is a daemon thread, meaning it will close when the main thread exits.
        pycam = threading.Thread(target=pycam_thread, args = (1,), daemon=True)
        pycam.start()

        alt_update = False
        gps_update = False
        imu_update = False
        #The radio driver program will control the time delays, since it can take up to 2 seconds to send a single message, or timeout
        while True:
            #Write Altimeter data only if it was started successfully
            if alt_active is True:
                #blocking mode
                with alt_lock:
                    alt_update = alt.update()
                    
                if alt_update != False:
                    radio.Send(alt_data_tag, alt_update)

            #Write gps data only if it was started successfully
            if gps_active is True:
                #blocking mode
                with gps_lock:                    
                    gps_update = gps.update()
                    
                if gps_update != False:
                    radio.Send(gps_data_tag, gps_update)               

            #Write imu data only if it was started successfully
            if imu_active is True:
                imu_update = imu.update()
                if imu_update != False:
                    radio.Send(imu_data_tag, imu_update)
               
            #If everything fails to send an update send a beacon 
            if alt_update==False and gps_update==False and imu_update==False:
                radio.Send(beacon_tag, "Sensors inactive!") #send any set a bytes here it is our beacon when no data is collected

    except KeyboardInterrupt:
       exit(1)

