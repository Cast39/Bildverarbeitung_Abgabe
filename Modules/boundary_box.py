import numpy as np
import cv2


def boundary_box(contour):

    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int32(box)
    center, size, angle = rect

    return (box, center, size, angle)
