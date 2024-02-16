import numpy as np
import cv2


def remove_background(image, colour=(5, 5, 5), tolerance=15):
    subject = np.float32(image)
    _,label,center = cv2.kmeans(subject,2,None,(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),10,cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    image = center[label.flatten()].reshape((image.shape))
    return image
