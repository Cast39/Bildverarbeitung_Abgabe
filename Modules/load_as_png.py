from cv2 import cvtColor, imread, COLOR_RGB2RGBA, error
from os import path


def loadAsPNG( file_path ):
    # try reading it
    if not (path.exists(file_path)):  # unless file doesn't exist
        return (-1, "file doesn't exist")
    try:
        return (0, cvtColor(imread(file_path), COLOR_RGB2RGBA))
    except error:
        return (-1, "couldn't read image from disk")
