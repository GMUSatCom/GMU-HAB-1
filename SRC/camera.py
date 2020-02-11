from picamera import PiCamera
from time import sleep
from datetime import datetime
def preview(function):
        def wrapper(self, *args, **kwargs):
            self.piCam.start_preview()
            return function(self, *args, **kwargs)
            self.piCam.stop_preview()
        return wrapper
#To do:
# print altidute, time, etc. onto the picture at bottom right corner. 
class Camera:
    def __init__(self, video_path, image_path):
        self.piCam = PiCamera()
        self.video_path
        self.image_path
        self.piCam.framerate = 30
        self.piCam.brightness = 50
        self.piCam.contrast = 50
		
    @preview
    def takePicture(self, x=2592, y=1944):
        # take picture
		# default res
        self.piCam.resolution = (x, y)
        now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        self.piCam.capture(self.image_path + now +'.jpg')
        sleep(2)
        close()
		
    @preview
    def takeVideo(self, x=640, y=480):
        # take a video
        # default res
        self.piCam.resolution = (x, y)
        now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        self.piCam.start_recording(self.video_path + now +'.h264')
        self.piCam.wait_recording(10)
        self.piCam.stop_recording()
        sleep(2)
        close()
		
    def close(self):
        self.piCam.close()