import numpy as np
import cv2


def crop(rotated_image,min_contour_size,crop_width,crop_hight):
    
    # Berechne das umschließende Rechteck nach der Rotation
    gray_rotated = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)
    _, binary_rotated = cv2.threshold(gray_rotated, 134, 255, cv2.THRESH_BINARY)
    contours_rotated, _ = cv2.findContours(binary_rotated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours_rotated:
        area = cv2.contourArea(contour)
        
        if area > min_contour_size:
            print(area)
            rect_rotated = cv2.minAreaRect(contour)
            box_rotated = cv2.boxPoints(rect_rotated)
            box_rotated = np.int0(box_rotated)
            center, size, angle = rect_rotated

            cv2.drawContours(rotated_image, [box_rotated], 0, (0, 255, 0), 2)

    
    # Definiere die gewünschte Größe des Ausgabebildes (einheitliche Größe)
    desired_size = (crop_width, crop_hight)  # Beispielgröße, anpassen nach Bedarf
    # Konvertiere die Eckpunkte des Rechtecks in das richtige Format für die Transformation
    src_points = np.float32([[box_rotated[1][0],box_rotated[1][1]], [box_rotated[0][0],box_rotated[0][1]], [box_rotated[2][0],box_rotated[2][1]], [box_rotated[3][0],box_rotated[3][1]]])#box_rotated
    dst_points = np.float32([[0, 0], [0, desired_size[1]], [desired_size[0], 0], [desired_size[0], desired_size[1]]])
    warped_pcb2 = cv2.getPerspectiveTransform(src_points, dst_points)
    warped_pcb2 = cv2.warpPerspective(rotated_image, warped_pcb2, desired_size)
    return warped_pcb2

    