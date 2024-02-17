from cv2 import getRotationMatrix2D, warpAffine


def align(image, center, angle, size=0):

    if angle > 45:
        angle -= 90
        # DEBUG: print("angle is bigger 45")

    # Rotiere das Bild um den Winkel
    align_matrix = getRotationMatrix2D(center, angle, scale=1)
    return warpAffine(image, align_matrix, (image.shape[1], image.shape[0]), image)
