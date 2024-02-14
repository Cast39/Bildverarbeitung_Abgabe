import numpy as np
import cv2


def remove_background(image, colour=(5, 5, 5), tolerance=15):
    param = cv2.SimpleBlobDetector.Params()
    param.filterByColor = True
    param.blobColor = 0
    param.minThreshold = 10
    param.maxThreshold = 150

    cv2.cvtColor(image, cv2.COLOR_RGB2RGBA, image)
    detector = cv2.SimpleBlobDetector()
    detector= detector.create(param)
    blobs = detector.detect(image)
    cv2.drawKeypoints(image, blobs, image, (0, 0, 0, 0))
    return image
