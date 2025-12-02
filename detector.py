import cv2
import time
from dx_capture import DXCapture
from utils import load_template

attempts = 0

with open("attempts.txt", "r+") as file:
    attempts = int(file.read())
    print(f"Attempts: {attempts}")

# ---- загрузка шаблона YOU DIED ----
template = load_template("you_died.png")
w, h = template.shape[::-1]

# ---- старт DXGI-захвата ----
capture = DXCapture(fps=30)
capture.start()

print("Детектор запущен!")
print("----------------------------------")

prev_time = time.time()

while True:
    frame = capture.get_frame()
    if frame is None:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # поиск в скриншоте
    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val > 0.62:
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 3)
        cv2.putText(frame, f"YOU DIED {max_val:.2f}",
                    (top_left[0], top_left[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        print(f"[DETECTED] YOU DIED! score={max_val:.3f}")
        attempts += 1
        print(f"Attempts now: {attempts}")
        print("----------------------------------")
        with open("attempts.txt", "w") as f:
            f.write(str(attempts))
        time.sleep(8)




capture.stop()
cv2.destroyAllWindows()
