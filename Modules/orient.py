import numpy as np
import cv2
import Modules.get_contours as contour
import Modules.get_biggest_contour as biggest

def orient(image):
    height, width = image.shape[:2]

    orientImage = image.copy()
    # Zentrum des Bildes berechnen
    center_x = width // 2
    center_y = height // 2
    image_center = (center_x,center_y)
    contour = biggest.get_biggest_contour(contour.get_contours(image))
    M = cv2.moments(contour)
    
    # Berechne die y-Koordinaten des Schwerpunkts
    if M["m00"] != 0:
        cY = int(M["m01"] / M["m00"])
    else:
        # Vermeide eine Division durch Null
        cY = 0
    
    
    if(cY > height//2):
        orient_matrix = cv2.getRotationMatrix2D(image_center, 180, scale=1)
        orientImage = cv2.warpAffine(image, orient_matrix, (image.shape[1], image.shape[0]))
    return orientImage