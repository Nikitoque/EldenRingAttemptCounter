import tkinter as tk
import json
import os
from PIL import Image, ImageTk

from detector import attempts
import overlay
import detector

# ---------- Глобальные переменные ----------
pressed = False
BG = "#1e1e1e"
FG = "#ffffff"
ENTRY_BG = "#2d2d2d"
ENTRY_FG = "#ffffff"
FONT = ("Segoe UI", 14)
BTN_PER_ROW = 3
PAD = 6


# ---------- Функции ----------
def load_data_on_start():
    if not os.path.exists("data.json"):
        return {"up_indent": "", "right_indent": "", "font_size": "", "color": "", "deaths": 0}
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_data():
    data = {
        "up_indent": entry_UI.get(),
        "right_indent": entry_RI.get(),
        "font_size": entry_fs.get(),
        "color": selected_color.get(),
        "deaths": attempts
    }
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Сохранено!")


def select_color(color):
    selected_color.set(color)
    print("Выбран цвет:", color)


def toggle_overlay():
    global pressed
    if not pressed:
        if detector.detector_running:
            return
        overlay.start_overlay()
        detector.start_detector()
        pressed = True
        print("Overlay started")
    else:
        overlay.stop_overlay()
        pressed = False
        print("Overlay stopped")


def reset_attempts():
    data = {
        "up_indent": entry_UI.get(),
        "right_indent": entry_RI.get(),
        "font_size": entry_fs.get(),
        "color": selected_color.get(),
        "deaths": 0
    }
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Сбросено!")
    deaths_title["text"] = f"Смертей: {data['deaths']}"


def update_label():
    with open("data.json", "r", encoding="utf-8") as f2:
        data2 = json.load(f2)
    deaths_title["text"] = f"Смертей: {data2['deaths']}"
    print(data2['deaths'])


def add_attempt():
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data["deaths"] += 1
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    deaths_title.config(text=f"Смертей: {data['deaths']}")


def subtract_attempt():
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    if data["deaths"] > 0:
        data["deaths"] -= 1
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    deaths_title.config(text=f"Смертей: {data['deaths']}")


# ---------- Инициализация окна ----------
root = tk.Tk()
root.title("ER Counter — Настройки")
root.geometry("400x850")
root.configure(bg=BG)
root.resizable(False, False)


data = load_data_on_start()
selected_color = tk.StringVar(value=data.get("color", ""))

# ---------- Фоновое изображение ----------
image = Image.open("img_1.png")
image = image.resize((500, 850))
bg_image = ImageTk.PhotoImage(image)
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# ---------- Функция создания поля ввода ----------
def create_entry_field(frame, text, default_value=""):
    sub_frame = tk.Frame(frame, bg=BG)
    label = tk.Label(sub_frame, text=text, font=FONT, bg=BG, fg=FG, width=16, anchor="e")
    entry = tk.Entry(sub_frame, bg=ENTRY_BG, fg=ENTRY_FG, font=FONT, width=12)
    entry.insert(0, default_value)
    label.pack(side="left", padx=5)
    entry.pack(side="left", padx=5)
    sub_frame.pack(pady=6, fill="x")
    return entry


# ---------- Секция 1: позиция и размер текста ----------
section1 = tk.Frame(root, bg=BG)
section1.pack(pady=(20, 10), fill="x")
tk.Label(section1, text="Позиция и размер текста", bg=BG, fg=FG, font=("Segoe UI", 18, "bold"))\
    .pack(pady=(0, 10))

entry_UI = create_entry_field(section1, "Отступ сверху:", data.get("up_indent", ""))
entry_RI = create_entry_field(section1, "Отступ справа:", data.get("right_indent", ""))
entry_fs = create_entry_field(section1, "Размер шрифта:", data.get("font_size", ""))


# ---------- Секция 2: цвет надписи ----------
section2 = tk.Frame(root, bg=BG)
section2.pack(pady=(25, 10))
tk.Label(section2, text="Цвет надписи", bg=BG, fg=FG, font=("Segoe UI", 18, "bold"))\
    .pack(pady=(0, 10))

colors_frame = tk.Frame(section2, bg=BG)
colors_frame.pack()
colors = ["blue", "cyan", "yellow", "white", "pink", "red"]
for index, color in enumerate(colors):
    btn = tk.Button(colors_frame, bg=color, width=6, height=2,
                    command=lambda c=color: select_color(c), relief="flat", bd=2)
    btn.grid(row=index // BTN_PER_ROW, column=index % BTN_PER_ROW, padx=PAD, pady=PAD)


# ---------- Секция 3: счётчик смертей ----------
section3 = tk.Frame(root, bg=BG)
section3.pack(pady=(25, 10), fill="x")
tk.Label(section3, text="Статистика", bg=BG, fg=FG, font=("Segoe UI", 18, "bold"))\
    .pack(pady=(0, 10))

deaths_title = tk.Label(section3, text=f"Смертей: {data['deaths']}", bg=BG, fg=FG,
                        font=("Segoe UI", 26, "bold"))
deaths_title.pack(pady=(0, 10))

# кнопки +1 / -1 / обновить
counter_frame = tk.Frame(section3, bg=BG)
counter_frame.pack(pady=(0, 10))
minus_btn = tk.Button(counter_frame, text="-1", command=subtract_attempt,
                      bg="#D9534F", fg="white", font=("Segoe UI", 18, "bold"), width=5)
minus_btn.pack(side="left", padx=10)
refresh_btn = tk.Button(counter_frame, text="Обновить", command=update_label,
                        bg="#3a3a3a", fg="white", font=("Segoe UI", 14), width=10)
refresh_btn.pack(side="left", padx=10)
plus_btn = tk.Button(counter_frame, text="+1", command=add_attempt,
                     bg="#4CAF50", fg="white", font=("Segoe UI", 18, "bold"), width=5)
plus_btn.pack(side="left", padx=10)

st_btn = tk.Button(section3, text="Сбросить попытки", command=reset_attempts,
                   bg="#3a3a3a", fg="white", font=("Segoe UI", 14), width=18)
st_btn.pack(pady=(0, 20))


# ---------- Секция 4: управление ----------
section4 = tk.Frame(root, bg=BG)
section4.pack(pady=(10, 20))
start_btn = tk.Button(section4, text="Старт / Стоп", command=toggle_overlay,
                      bg="#FFD700", fg="black", font=("Segoe UI", 20, "bold"), width=18)
start_btn.pack(pady=5)
save_btn = tk.Button(section4, text="Сохранить данные", command=save_data,
                     bg="#3a3a3a", fg="white", font=("Segoe UI", 16), width=18)
save_btn.pack(pady=5)


# ---------- Запуск ----------
root.mainloop()
