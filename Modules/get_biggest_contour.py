import numpy as np
import cv2

def get_biggest_contour(contours):

    return max(contours, key=cv2.contourArea)
            

