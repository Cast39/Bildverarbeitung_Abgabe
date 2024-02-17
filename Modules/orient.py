from cv2 import rotate, moments, split, ROTATE_90_CLOCKWISE, ROTATE_180
from numpy import floor_divide

def orient(image):
    height, width = image.shape[:2]

    # case of perfect vertical alignement
    if height > width:
        rotate(image, ROTATE_90_CLOCKWISE, image)

    # define vertical center
    b,_,_,_ = split(image)
    M = moments(floor_divide(b,127), True)

    # Vermeide eine Division durch Null
    if M["m00"] != 0:
        # Berechne die y-Koordinaten des Schwerpunkts
        cY = int(M["m01"] / M["m00"])
    else:
        cY = 0

    if cY > height // 2:
        rotate(image, ROTATE_180, image)
    return image
