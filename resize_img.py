from screeninfo import get_monitors
from PIL import Image

def ResizeImg():
    #monitor
    start_screen_width = 2560
    start_screen_height = 1440

    for monitor in get_monitors():
        print(f"---resize_img script connected!---")
        new_screen_height = monitor.height
        new_screen_width = monitor.width

    #file
    try:
        img = Image.open("you_died.png")
        img_width = img.width
        img_height = img.height
    except FileNotFoundError:
        print("File is not founded")
    except Exception as e:
        print(f"Error: {e}")

    new_img_width = int((img_width * new_screen_width) / start_screen_width)
    new_img_height = int((img_height * new_screen_height) / start_screen_height)

    new_size = (new_img_width, new_img_height)
    new_img = img.resize(new_size)
    new_img.save("you_died_resized.png")

    if start_screen_width != new_screen_width or start_screen_height != new_screen_height:
        print("----!resize_img script started!---")
        print(f"start img size: {img_width}x{img_height}")
        print(f"new img size: {new_img_width}x{new_img_height}")