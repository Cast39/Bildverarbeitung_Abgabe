import cv2

def orient(image):
    ret = image.copy()
    height, width = image.shape[:2]

    # case of perfect vertical alignement
    if height > width:
        ret = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    # define vertical center
    _,_,b,_ = cv2.split(image)
    M = cv2.moments(b, True)

    # Vermeide eine Division durch Null
    if M["m00"] != 0:
        # Berechne die y-Koordinaten des Schwerpunkts
        cY = int(M["m01"] / M["m00"])
    else:
        cY = 0

    if cY > height // 2:
        ret = cv2.rotate(image, cv2.ROTATE_180)
    return ret
