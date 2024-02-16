import cv2

# so simple it will never be refactored, or optimized 
# ??? TODO merge with "get_contours" to form "get_contour"???

def get_biggest_contour(contours):

    return max(contours, key=cv2.contourArea)
            

