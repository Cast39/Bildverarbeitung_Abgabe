import numpy as np
import cv2
from Modules.get_contours import get_contours
from Modules.get_biggest_contour import get_biggest_contour


def orient(image):
    height, width = image.shape[:2]

    orientImage = image.copy()
    # Zentrum des Bildes berechnen
    center_x = width // 2
    center_y = height // 2
    image_center = (center_x, center_y)
    contour = get_biggest_contour(get_contours(image))
    M = cv2.moments(contour)

    # Vermeide eine Division durch Null
    if M["m00"] != 0:
        # Berechne die y-Koordinaten des Schwerpunkts
        cY = int(M["m01"] / M["m00"])
    else:
        cY = 0

    if cY > height // 2:
        orient_matrix = cv2.getRotationMatrix2D(image_center, 180, scale=1)
        orientImage = cv2.warpAffine(
            image, orient_matrix, (image.shape[1], image.shape[0])
        )
    return orientImage
