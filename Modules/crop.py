import cv2
import numpy as np


def crop(image, box, aspect_ratio=980/565):

    # Koordinaten der Box extrahieren
    x, y, w, h = cv2.boundingRect(box)

    # case pins are deformed over board
    box_aspect_ratio = np.round(w/h,1)
    aspect_ratio = np.round(aspect_ratio,1)
    if (box_aspect_ratio>aspect_ratio):
        vert_pad = int((aspect_ratio * w) // h)
    else:
        vert_pad = 1

    # Bildausschnitt basierend auf den Boxkoordinaten und padding ausschneiden
    cropped_image = image[
        (y - (vert_pad + h)) : (y + h), 
        (x) : (x + w)
    ]
    return cropped_image
