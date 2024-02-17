import cv2
import os


def loadAsPNG( file_path ):
    # try reading it
    if not (os.path.exists(file_path)):  # unless file doesn't exist
        return (-1, "file doesn't exist")
    try:
        return (0, cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_RGB2RGBA))
    except cv2.error:
        return (-1, "couldn't read image from disk")
