import numpy as np
import cv2

def get_biggest_contour(contours):
    biggest_area = 0.0
    i = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        # Überprüfe, ob die Fläche größer als die Mindestkonturgröße ist
        if area > biggest_area:
            biggest_area = area
            result_i = i


        i +=1
    return contours[result_i]
            

