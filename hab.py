import os
from camera import *
from gps import *
from alt import *

print("boi")
cam = Camera()
gps = Gps()
alt = Alt()

gps.read_serial('/dev/ttyS0')
alt.write_data()
#cam.takePicture()
#cam.takePicture()
#cam.takeVideo()

cam.close()

