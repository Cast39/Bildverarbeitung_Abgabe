import numpy as np
import cv2


def segmentierung(image):
    seg_img = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

    # Aufteilen des Bildes in die einzelnen Kanäle (RGBA)
    r, g, b, _ = cv2.split(seg_img)

    # Bedingungsmaske für jede Klasse definieren
    # Klasse 1: Rot
    mask_black = (r < 100) & (g < 100) & (b < 100)
    seg_img[mask_black] = (0, 0, 0, 0)

    return seg_img
