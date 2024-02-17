from cv2 import cvtColor, findContours, contourArea,  COLOR_RGBA2GRAY, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE

def get_contour(image):
    # Berechne das umschließende Rechteck nach der Rotation
    gray = cvtColor(image, COLOR_RGBA2GRAY)
    #FEATURE-BRANCH: gray = cv2.bitwise_not(gray)
    contours, _ = findContours(gray, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
    return max(contours, key=contourArea)
            

