import threading
import time
import cv2
import json

from dx_capture import DXCapture
from utils import load_template
from resize_img import ResizeImg
import overlay


capture = None
with open("data.json", "r") as f:
    data = json.load(f)

attempts = int(data.get("deaths"))
detector_running = False


def detector_thread():
    global capture, attempts, detector_running

    detector_running = True

    # Загружаем JSON
    with open("data.json", "r") as f:
        data = json.load(f)

    attempts = int(data.get("deaths", 0))
    overlay.safe_update_label(f"Deaths: {attempts}")

    ResizeImg()

    template = load_template("you_died_resized.png")
    w, h = template.shape[::-1]

    capture = DXCapture(fps=30)
    capture.start()

    while overlay.running and detector_running:
        frame = capture.get_frame()
        if frame is None:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        if max_val > 0.65:
            attempts += 1

            with open("data.json", "r") as f:
                data = json.load(f)

            data["deaths"] = attempts

            with open("data.json", "w") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            overlay.safe_update_label(f"Deaths: {attempts}")


            time.sleep(8)

    if capture:
        try:
            capture.stop()
        except:
            pass

    capture = None
    detector_running = False


def start_detector():
    """Запускает детектор, если он не запущен"""
    if detector_running:
        return

    threading.Thread(target=detector_thread, daemon=True).start()


def stop_detector():
    """Останавливает цикл детектора"""
    global detector_running
    detector_running = False
