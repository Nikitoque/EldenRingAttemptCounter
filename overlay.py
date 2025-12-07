import tkinter as tk
import ctypes
import json

overlay = None
label = None
running = False


def start_overlay():
    """Создание окна и запуск цикла"""
    global overlay, label, running

    if overlay is not None:
        return  # уже запущено

    with open("data.json", "r") as f:
        data = json.load(f)

    overlay = tk.Toplevel()
    overlay.overrideredirect(True)
    overlay.attributes("-topmost", True)
    overlay.config(bg="magenta")
    overlay.wm_attributes("-transparentcolor", "magenta")

    label = tk.Label(
        overlay,
        text="Attempts: 0",
        font=("Segoe UI", int(data["font_size"]), "bold"),
        fg=data["color"],
        bg="magenta"
    )
    label.pack()

    # позиция
    overlay.update_idletasks()
    screen_w = overlay.winfo_screenwidth()
    w = label.winfo_reqwidth()
    x = screen_w - w - int(data["right_indent"])
    y = int(data["up_indent"])
    overlay.geometry(f"+{x}+{y}")

    running = True
    update_loop()


def update_loop():
    """Цикл обновления overlay"""
    global overlay, running

    if not running or overlay is None:
        return  # прекращаем цикл!

    try:
        overlay.update()
    except:
        overlay = None
        return

    overlay.after(15, update_loop)


def stop_overlay():
    """Корректное закрытие окна"""
    global overlay, running

    running = False

    if overlay is not None:
        try:
            overlay.destroy()
        except:
            pass

    overlay = None


def safe_update_label(text):
    if label:
        try:
            label.after(0, lambda: label.config(text=text))
        except:
            pass
