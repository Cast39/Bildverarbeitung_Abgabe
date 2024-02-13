import numpy as np
import cv2

def align(image,center,angle):

    if(angle > 45):
        angle -= 180
 
    alignImage = image.copy()
    # Rotiere das Bild um den Winkel
    align_matrix = cv2.getRotationMatrix2D(center, angle, scale=1)
    alignImage = cv2.warpAffine(alignImage, align_matrix, (alignImage.shape[1], alignImage.shape[0]))
    return alignImage