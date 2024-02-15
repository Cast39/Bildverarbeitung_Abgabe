import numpy as np
import cv2

#Segmentierung zerpflckt Bild zu stark, TODO: Blobanalyse o.Ä.

def segmentierung(image):
    # Aufteilen des Bildes in die einzelnen Kanäle (RGBA)
    r, g, b, _ = cv2.split(image)

    # Bedingungsmaske für jede Klasse definieren
    # Klasse 1: Rot
    mask_black = (r < 100) & (g < 100) & (b < 100)
    image[mask_black] = (0, 0, 0, 0)

    return image
