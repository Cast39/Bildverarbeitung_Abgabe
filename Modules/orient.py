import cv2
import numpy as np

def orient(image):
    height, width = image.shape[:2]

    # case of perfect vertical alignement
    if height > width:
        cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE, image)

    # define vertical center
    b,_,_,_ = cv2.split(image)
    M = cv2.moments(np.floor_divide(b,127), True)

    # Vermeide eine Division durch Null
    if M["m00"] != 0:
        # Berechne die y-Koordinaten des Schwerpunkts
        cY = int(M["m01"] / M["m00"])
    else:
        cY = 0

    if cY > height // 2:
        cv2.rotate(image, cv2.ROTATE_180, image)
    return image
