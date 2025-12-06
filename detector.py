import threading
import time
import cv2
from dx_capture import DXCapture
from overlay import data_json
from utils import load_template
from resize_img import ResizeImg
import overlay
import json


def detector_thread():


    attempts = int(data_json["deaths"])
    overlay.safe_update_label(f"Attempts: {attempts}")
    print("-----overlay script connected!----")


    ResizeImg()

    template = load_template("you_died_resized.png")
    w, h = template.shape[::-1]

    capture = DXCapture(fps=30)
    capture.start()

    print("--------Detector started!---------")
    print("----------------------------------")

    while True:
        frame = capture.get_frame()
        if frame is None:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val > 0.62:
            attempts += 1
            data_json["deaths"] = attempts

            with open("data.json", "w") as f:
                json.dump(data_json, f, indent=4, ensure_ascii=False)

            overlay.safe_update_label(f"Attempts: {attempts}")

            print(f"[DETECTED] YOU DIED! attempts={attempts}")
            print("----------------------------------")

            time.sleep(8)


threading.Thread(target=detector_thread, daemon=True).start()

overlay.start_overlay()
