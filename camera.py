from picamera import PiCamera
from time import sleep
from datetime import datetime

#To do:
# print altidute, time, etc. onto the picture at bottom right corner. 

class Camera:
    def __init__(self):
        self.piCam = PiCamera()
        
        self.piCam.framerate = 30
        self.piCam.brightness = 50
        self.piCam.contrast = 50
    
    def takePicture(self, x=2592, y=1944):
        # take picture
        # self.piCam.start_preview() # default res
        self.piCam.resolution = (x, y)
        now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        self.piCam.capture('/home/pi/hab/imgs/' + now +'.jpg')
        # self.piCam.stop_preview()
        sleep(2)
        
    def takeVideo(self, x=640, y=480):
        # take a video
        # self.piCam.start_preview() # default res
        self.piCam.resolution = (x, y)
        now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        self.piCam.start_recording('/home/pi/hab/vids/' + now +'.h264')
        self.piCam.wait_recording(10)
        self.piCam.stop_recording()
        # self.piCam.stop_preview()
        sleep(2)
        
    def close(self):
        self.piCam.close()
        
        

