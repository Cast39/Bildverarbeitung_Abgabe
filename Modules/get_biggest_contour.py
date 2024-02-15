import numpy as np
import cv2

def get_biggest_contour(contours):

    return max(contours, key=cv2.contourArea)
            
def get_biggest_contours(contours):
    ret = []
    for contour in contours:
        if cv2.contourArea(contour) > 10000:
            ret.append(contour)

    return ret

