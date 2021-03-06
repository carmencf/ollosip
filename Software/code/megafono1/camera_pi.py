import io
import time
import picamera
from base_camera import BaseCamera


class Camera(BaseCamera):
    
   
        
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            camera.resolution=(720,480)
            camera.framerate=30
            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
    def resolucion(res):
            camera.resolution=(res)