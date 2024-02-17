import numpy as np
import cv2


def align(image, center, angle, size=0):

    if angle > 45:
        angle -= 90
        # DEBUG: print("angle is bigger 45")

    # Rotiere das Bild um den Winkel
    align_matrix = cv2.getRotationMatrix2D(center, angle, scale=1)
    return cv2.warpAffine(image, align_matrix, (image.shape[1], image.shape[0]), image)
