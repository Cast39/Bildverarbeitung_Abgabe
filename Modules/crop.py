from cv2 import boundingRect
from numpy import round


def crop(image, box, aspect_ratio=980 / 580):

    # Koordinaten der Box extrahieren
    x, y, w, h = boundingRect(box)

    # case pins are deformed over board
    box_aspect_ratio = round(w / h, 2)
    aspect_ratio = round(aspect_ratio, 2)
    if box_aspect_ratio > aspect_ratio:
        vert_pad = int((w // aspect_ratio) - h)
    else:
        vert_pad = 0

    # Bildausschnitt basierend auf den Boxkoordinaten und padding ausschneiden
    return image[(y - vert_pad) : (y + h), (x) : (x + w)]
    