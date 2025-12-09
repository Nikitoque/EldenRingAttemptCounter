import tkinter as tk
import json
import os
from PIL import Image, ImageTk
from setuptools.logging import configure

from detector import attempts
import overlay
import detector

def start_detector():
        import overlay
        import detector
        overlay.start_overlay()


# ---------- Загрузка JSON ----------
def load_data_on_start():
    if not os.path.exists("data.json"):
        return {"up_indent": "", "right_indent": "", "font_size": "", "color": "", "deaths": ""}
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ---------- Сохранение ----------
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

# ---------- Выбор цвета ----------
def select_color(color):
    selected_color.set(color)
    print("Выбран цвет:", color)

pressed = False

def toggle_overlay():
    global pressed

    if not pressed:
        if detector.detector_running:
            return  # защита от двойного запуска

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
    print("Сохранено!")

    global deaths_title
    deaths_title["text"] = f"Смертей: {data["deaths"]}"

def update_lable():
    with open("data.json", "r", encoding="utf-8") as f2:
        data2 = json.load(f2)

    global deaths_title
    deaths_title["text"] = f"Смертей: {data2["deaths"]}"
    print(data2["deaths"])

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

    if data["deaths"] > 0:      # защита от отрицательных значений
        data["deaths"] -= 1

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    deaths_title.config(text=f"Смертей: {data['deaths']}")



# ---------- Тёмная тема ----------
BG = "#1e1e1e"
FG = "#ffffff"
ENTRY_BG = "#2d2d2d"
ENTRY_FG = "#ffffff"
FONT = ("Segoe UI", 14)

root = tk.Tk()
root.title("ER Counter — Настройки")
root.geometry("700x620")
root.configure(bg=BG)

data = load_data_on_start()
selected_color = tk.StringVar(value=data.get("color", ""))

# ---------- Загружаем изображение ----------
image = Image.open("img.png")  # путь к вашему изображению
image = image.resize((700, 620))      # масштабируем под размер окна
bg_image = ImageTk.PhotoImage(image)
root.resizable(False, False)

# ---------- Создаём Label с изображением ----------
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # растягиваем на весь фон

# ---------- Поля ввода ----------
entry_UI = tk.Entry(root, bg=ENTRY_BG, fg=ENTRY_FG, font=FONT, width=12)
entry_RI = tk.Entry(root, bg=ENTRY_BG, fg=ENTRY_FG, font=FONT, width=12)
entry_fs = tk.Entry(root, bg=ENTRY_BG, fg=ENTRY_FG, font=FONT, width=12)

entry_UI.insert(0, data.get("up_indent", ""))
entry_RI.insert(0, data.get("right_indent", ""))
entry_fs.insert(0, data.get("font_size", ""))

# ---------- Функция добавления строки ----------
def add_row(label_text, entry_widget, row):
    label = tk.Label(root, text=label_text, font=FONT, bg=BG, fg=FG, width=14, anchor="e")
    label.grid(row=row, column=0, padx=10, pady=8, sticky="e")
    entry_widget.grid(row=row, column=1, padx=10, pady=8, sticky="w")

# ---------- Добавляем строки ----------
add_row("Отступ сверху:", entry_UI, 0)
add_row("Отступ справа:", entry_RI, 1)
add_row("Размер шрифта:", entry_fs, 2)

# ---------- Надпись Цвета ----------
color_title = tk.Label(root, text="Цвета:", bg=BG, fg=FG, font=FONT)
color_title.grid(row=3, column=0, columnspan=3, pady=(15, 5))

# ---------- Цветовые кнопки ----------
colors_frame = tk.Frame(root, bg=BG)
colors_frame.grid(row=4, column=0, columnspan=3, pady=10)

colors = [
    "blue", "cyan", "yellow",
    "white", "pink", "red"
]

BTN_PER_ROW = 3
PAD = 6

for index, color in enumerate(colors):
    r = index // BTN_PER_ROW
    c = index % BTN_PER_ROW
    btn = tk.Button(
        colors_frame,
        bg=color,
        width=4,
        height=2,
        command=lambda c=color: select_color(c),
        relief="flat"
    )
    btn.grid(row=r, column=c, padx=PAD, pady=PAD)

# ---------- Настройка растяжения строк ----------
root.grid_rowconfigure(5, weight=1)  # Пустая растяжимая строка перед кнопкой
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)


deaths_title = tk.Label(root, text=f"Смертей: {data["deaths"]}", bg=BG, fg=FG, font=("Segoe UI", 22))
deaths_title.grid(row=5, column=0, columnspan=2, pady=5)


# ---------- Кнопка Сохранить ----------
save_btn = tk.Button(
    root,
    text="Сохранить данные",
    command=save_data,
    bg="#3a3a3a",
    fg="white",
    font=FONT,
    width=16,
    height=1
)
save_btn.grid(row=7, column=0, columnspan=3, pady=5)

start_btn = tk.Button(
    root,
    text="Старт / Стоп",
    command=toggle_overlay,
    bg="#FFD700",
    fg="black",
    font=("Segoe UI", 18, "bold"),
    width=16,
    height=1
)

start_btn.grid(row=8, column=0, columnspan=3, pady=5, padx =5)

st_btn = tk.Button(
    root,
    text="Сбросить попытки",
    command=reset_attempts,
    bg="#3a3a3a",
    fg="white",
    font=FONT,
    width=16,
    height=1
)
st_btn.grid(row=6, column=0, columnspan=3, pady=5, padx =5)

rs_btn = tk.Button(
    root,
    text="Обновить",
    command=update_lable,
    bg="#3a3a3a",
    fg="white",
    font=FONT,
    width=8,
    height=1
)
rs_btn.grid(row=5, column=1, columnspan=1, pady=5, padx =5)

plus_btn = tk.Button(
    root,
    text="+1",
    command=add_attempt,
    bg="#4CAF50",
    fg="white",
    font=("Segoe UI", 18, "bold"),
    width=5,
    height=1
)
plus_btn.grid(row=5, column=2, pady=5, padx=5)


minus_btn = tk.Button(
    root,
    text="-1",
    command=subtract_attempt,
    bg="#D9534F",
    fg="white",
    font=("Segoe UI", 18, "bold"),
    width=5,
    height=1
)
minus_btn.grid(row=6, column=2, pady=5, padx=5)



root.mainloop()
