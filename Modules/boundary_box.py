from numpy import int32
from cv2 import minAreaRect, boxPoints


def boundary_box(contour):

    rect = minAreaRect(contour)
    box = boxPoints(rect)
    box = int32(box)
    center, size, angle = rect

    return (box, center, size, angle)
