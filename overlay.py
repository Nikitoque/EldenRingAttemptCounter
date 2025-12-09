import tkinter as tk
import json
import detector

overlay = None
label = None
running = False


def stop_overlay():
    global overlay, running

    running = False

    # Остановить DXCam корректно
    detector.stop_detector()

    if detector.capture:
        try:
            detector.capture.stop()
        except:
            pass
        detector.capture = None

    if overlay is not None:
        try:
            overlay.destroy()
        except:
            pass

    overlay = None


def start_overlay():
    global overlay, label, running

    if overlay is not None:
        return  # уже работает

    with open("data.json", "r") as f:
        data = json.load(f)

    overlay = tk.Toplevel()
    overlay.overrideredirect(True)
    overlay.attributes("-topmost", True)
    overlay.config(bg="magenta")
    overlay.wm_attributes("-transparentcolor", "magenta")

    label = tk.Label(
        overlay,
        text="Deaths: 0",
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
    global overlay, running

    if not running or overlay is None:
        return

    try:
        overlay.update()
    except:
        overlay = None
        return

    overlay.after(15, update_loop)



def safe_update_label(text):
    if label:
        try:
            label.after(0, lambda: label.config(text=text))
        except:
            pass
