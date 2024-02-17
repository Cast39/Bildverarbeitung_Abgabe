import cv2

# Segmentierung zerpfülckt Bild zu stark, TODO: Blobanalyse o.Ä.


def segment(image):
    # Aufteilen des Bildes in die einzelnen Kanäle (RGBA)
    r, g, b, _ = cv2.split(image)

    # Bedingungsmaske für jede Klasse definieren
    # Klasse 1: Rot
    mask_black = (r < 133) & (g < 133) & (b < 150)
    image[mask_black] = (0, 0, 0, 0)

    return image
