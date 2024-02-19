import numpy as np
from cv2 import minAreaRect, boxPoints, moments

def get_boundary_from_contour(contour):
    rect = minAreaRect(contour)
    box = boxPoints(rect)
    box = np.int32(box)
    center, size, angle = rect

    return (box, center, size, angle)


def get_boundary_from_graph(contour_graph):
    angles = contour_graph[:, 0]
    radia = contour_graph[:, 1]
    angles = contour_graph[:, 2]
    box = boxPoints(rect)
    box = int32(box)
    center, size, angle = rect

    return (box, center, size, angle)