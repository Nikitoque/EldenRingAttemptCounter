from window_capture import WindowCapture
from detector import YouDiedDetector
import time

def main():
    wc = WindowCapture("full_screenshot.png")   # имя окна
    detector = YouDiedDetector("you_died.png")

    print("Стартуем мониторинг окна...")

    while True:
        frame = wc.get_frame()
        found, val = detector.detect(frame)

        if found:
            print(f"YOU DIED найдено! match={val:.3f}")
        else:
            print(f"нет совпадения: {val:.3f}")

        time.sleep(0.1)

if __name__ == "__main__":

    main()
