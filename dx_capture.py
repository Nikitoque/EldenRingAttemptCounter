import dxcam
import time

class DXCapture:
    def __init__(self, fps=30, region=None):
        self.camera = dxcam.create(output_color="BGR")
        self.fps = fps
        self.region = region

    def start(self):
        self.camera.start(target_fps=self.fps, region=self.region)
        time.sleep(0.1)

    def get_frame(self):
        return self.camera.get_latest_frame()

    def stop(self):
        try:
            self.camera.stop()
        except:
            pass