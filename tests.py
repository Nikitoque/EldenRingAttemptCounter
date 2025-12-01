import cv2
import numpy as np
from window_capture import WindowCapture  # твой класс для захвата окна

# === Настройки ===
WINDOW_NAME = "full_screenshot.png"  # точное название окна игры
TEMPLATE_FILE = "you_died.png"
THRESHOLD = 0.8  # порог уверенного совпадения

# === Создаём объект захвата окна ===
try:
    wc = WindowCapture(WINDOW_NAME)
    frame = wc.get_frame()
except Exception as e:
    print(f"Не удалось захватить окно {WINDOW_NAME}: {e}")
    exit()

frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# === Загружаем шаблон YOU DIED ===
template = cv2.imread(TEMPLATE_FILE)
if template is None:
    print(f"Ошибка: {TEMPLATE_FILE} не найден!")
    exit()
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
th, tw = template_gray.shape[:2]

# === Поиск шаблона в кадре ===
result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

print("max_val:", max_val)
print("max_loc:", max_loc)

# === Рисуем рамку, если совпадение достаточно точное ===
if max_val >= THRESHOLD:
    top_left = max_loc
    bottom_right = (top_left[0] + tw, top_left[1] + th)

    # копируем кадр, чтобы он был записываемым
    frame_copy = frame.copy()

    cv2.rectangle(frame_copy, top_left, bottom_right, (0, 0, 255), 3)
    cv2.putText(frame_copy, f"{max_val:.3f}", (top_left[0], top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    print("Надпись обнаружена!")

    cv2.imwrite("result_window.png", frame_copy)
    print("Файл result_window.png сохранён.")
else:
    print("Надпись не найдена.")

# === Сохраняем результат для проверки ===
cv2.imwrite("result_window.png", frame)
print("Файл result_window.png сохранён.")
