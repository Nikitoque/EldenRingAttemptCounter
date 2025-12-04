import tkinter as tk
import ctypes

GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.8)

transparent_color = "magenta"
root.config(bg=transparent_color)
root.wm_attributes("-transparentcolor", transparent_color)

label = tk.Label(root, text="Attempts: 0", font=("Segoe UI", 16, "bold"),
                 bg=transparent_color, fg="white")
label.pack()

screen_width = root.winfo_screenwidth()
label.update_idletasks()
w = label.winfo_reqwidth()
x = screen_width - w - 100
y = 10
root.geometry(f"+{x}+{y}")

hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE,
                                    style | WS_EX_LAYERED | WS_EX_TRANSPARENT)


def safe_update_label(text):
    root.after(0, lambda: label.config(text=text))


def start_overlay():
    root.mainloop()
