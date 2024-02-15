import numpy as np
import cv2

def sigmentierung(image):

    height, width = image.shape[:2]
    segmented_image = np.zeros((height, width, 3), dtype=np.uint8)

    # Aufteilen des Bildes in die einzelnen Kanäle (B, G, R)
    b, g, r = cv2.split(image)

    # Bedingungsmaske für jede Klasse definieren
    # Klasse 1: Rot
    mask_black = ((r < 134) & (g < 134) & (b < 134))
    segmented_image[mask_black] = (255, 255, 255)


    return segmented_image