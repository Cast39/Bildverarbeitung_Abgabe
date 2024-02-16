import cv2

def get_contour(image):
    # Berechne das umschließende Rechteck nach der Rotation
    gray = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
    #FEATURE-BRANCH: gray = cv2.bitwise_not(gray)
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return max(contours, key=cv2.contourArea)
            

