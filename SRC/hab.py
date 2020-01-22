import os
import time
import threading
import board
import busio
from camera import *
from gps import *
from alt import *
from imu import *
from radio import *
from os import *

#TODO:
#run hab.py on startup
#camera thread might need its own instance of the altimiter and gps modules?

sensor_poll_rate = .5
#Primary ic bus
i2c_port = busio.I2C(board.SCL, board.SDA)
#install root path 
root_dir = path.dirname(path.realpath(__file__))
csv_dir = root_dir+'/data'
print("Working directory: "+root_dir)
print("Captured data directory: "+csv_dir)
#Create the gps object with the file paths and gps serial path
gps = Gps(csv_dir+'/gps.csv', '/dev/ttyS0' )
#Create the altimiter object and initialize it 
alt = Alt(csv_dir+'/alt.csv', i2c_port)
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
    except:
        print("Could not make directories, exiting")
        exit(0)

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

            cam.close()
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
        while True:

            #Write Altimeter data only if it was started successfully
            if alt_active is True:
                alt_update = alt.update()
                if alt_update != False:
                    radio.Send(alt_data_tag, var)
                else:
                    radio.Send(alt_data_tag, "Failure")

            #Write gps data only if it was started successfully
            if gps_active is True:
                gps_update = gps.update()
                if gps_update != False:
                    radio.Send(gps_data_tag, var)
                else:
                    radio.Send(gps_data_tag, "Failure")

            #Write imu data only if it was started successfully
            if imu_active is True:
                imu_update = imu.update()
                if imu_update != False:
                    radio.Send(imu_data_tag, var)
                else:
                    radio.Send(imu_data_tag,"Failure")

            #If everything fails to send an update send a beacon 
            if (alt_update and gps_update and imu_update)== False:
                radio.Send(beacon_tag, "Beacon!") #send any set a bytes here it is our beacon when no data is sent

            time.sleep(sensor_poll_rate)

    except KeyboardInterrupt:
       exit(1)

