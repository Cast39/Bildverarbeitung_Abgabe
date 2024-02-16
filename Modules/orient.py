import numpy as np
import cv2
from Modules.get_contours import get_contours
from Modules.get_biggest_contour import get_biggest_contour


def orient(image):
    ret = image.copy()
    height, width = image.shape[:2]

    # case of perfekt vertical alignement
    if height > width:
        ret = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    # define vertical center
    contour = get_biggest_contour(get_contours(ret))
    M = cv2.moments(contour)

    # Vermeide eine Division durch Null
    if M["m00"] != 0:
        # Berechne die y-Koordinaten des Schwerpunkts
        cY = int(M["m01"] / M["m00"])
    else:
        cY = 0

    if cY > height // 2:
        ret = cv2.rotate(image, cv2.ROTATE_180)
    return ret
