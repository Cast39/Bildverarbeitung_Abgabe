import numpy as np
import cv2


def get_box(contours,min_contour_size):
        
    for contour in contours:

        area = cv2.contourArea(contour)
        
        if area > min_contour_size:

            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            center, size, angle = rect

    return (box,center,angle)
