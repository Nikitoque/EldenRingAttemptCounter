import cv2

def load_template(path):
    template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Не удалось загрузить шаблон: {path}")
    return template
