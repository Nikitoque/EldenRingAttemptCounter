import tkinter as tk
import ctypes
import json

with open("data.json", "r") as f:
    data_json = json.load(f)

GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020

overlay = tk.Toplevel()
overlay.overrideredirect(True)
overlay.attributes("-topmost", True)
overlay.attributes("-alpha", 0.8)

transparent_color = "magenta"
overlay.config(bg=transparent_color)
overlay.wm_attributes("-transparentcolor", transparent_color)

label = tk.Label(overlay, text="Attempts: 0", font=("Segoe UI", int(data_json["font_size"]), "bold"),
                 bg=transparent_color, fg=data_json["color"])
label.pack()

screen_width = overlay.winfo_screenwidth()
label.update_idletasks()
w = label.winfo_reqwidth()
x = screen_width - w - int(data_json["right_indent"])
y = int(data_json["up_indent"])
overlay.geometry(f"+{x}+{y}")

hwnd = ctypes.windll.user32.GetParent(overlay.winfo_id())
style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE,
                                    style | WS_EX_LAYERED | WS_EX_TRANSPARENT)


def safe_update_label(text):
    overlay.after(0, lambda: label.config(text=text))


def start_overlay():
    overlay.mainloop()
