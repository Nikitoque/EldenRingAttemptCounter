import win32gui
import win32ui
import win32con
import numpy as np
import cv2

class WindowCapture:
    def __init__(self, window_name=None):
        self.hwnd = win32gui.FindWindow(None, window_name)

        if not self.hwnd:
            raise Exception(f"Окно '{window_name}' не найдено")

        rect = win32gui.GetWindowRect(self.hwnd)
        self.w = rect[2] - rect[0]
        self.h = rect[3] - rect[1]

    def get_frame(self):
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfcDC, self.w, self.h)
        saveDC.SelectObject(bitmap)

        saveDC.BitBlt((0, 0), (self.w, self.h), mfcDC, (0, 0), win32con.SRCCOPY)

        bmp_bytes = bitmap.GetBitmapBits(True)
        img = np.frombuffer(bmp_bytes, dtype=np.uint8).reshape((self.h, self.w, 4))

        # чистим мусор
        win32gui.DeleteObject(bitmap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)

        # убираем alpha-канал
        return img[:, :, :3]
