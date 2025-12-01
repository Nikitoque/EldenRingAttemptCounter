import cv2
import numpy as np

class YouDiedDetector:
    def __init__(self, template_path="you_died.png", threshold=0.8):
        self.template = cv2.imread(template_path)
        self.template = cv2.cvtColor(self.template, cv2.COLOR_BGR2GRAY)
        self.th = threshold

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray, self.template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        return max_val >= self.th, max_val
