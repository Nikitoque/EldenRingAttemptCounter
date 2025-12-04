import cv2
import time
from dx_capture import DXCapture
from utils import load_template
from  resize_img import ResizeImg

with open("attempts.txt", "r+") as file:
    attempts = int(file.read())
    print(f"Attempts: {attempts}")

ResizeImg()

template = load_template("you_died_resized.png")
w, h = template.shape[::-1]

capture = DXCapture(fps=30)
capture.start()

print("Detector started!")
print("----------------------------------")

prev_time = time.time()

while True:
    frame = capture.get_frame()
    if frame is None:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val > 0.62:
        print(f"[DETECTED] YOU DIED! score={max_val:.3f}")
        attempts += 1
        print(f"Attempts now: {attempts}")
        print("----------------------------------")
        with open("attempts.txt", "w") as f:
            f.write(str(attempts))
        time.sleep(8)