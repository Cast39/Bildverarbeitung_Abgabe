import cv2

# Segmentierung zerpfülckt Bild zu stark, TODO: Blobanalyse o.Ä.

def segment(image):
    ret = image.copy()
    # Aufteilen des Bildes in die einzelnen Kanäle (RGBA)
    r, g, b, _ = cv2.split(image)

    # Bedingungsmaske für jede Klasse definieren
    # Klasse 1: Rot
    mask_black = (r < 110) & (g < 110) & (b < 110)
    ret[mask_black] = (0, 0, 0, 0)

    return ret
