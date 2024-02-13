import numpy as np
import cv2


def scale(image,box):

     # Definiere die gewünschte Größe des Ausgabebildes (einheitliche Größe)
    desired_size = (980, 565)  # Beispielgröße, anpassen nach Bedarf
    # Konvertiere die Eckpunkte des Rechtecks in das richtige Format für die Transformation
    src_points = np.float32([[box[1][0],box[1][1]], [box[0][0],box[0][1]], [box[2][0],box[2][1]], [box[3][0],box[3][1]]])#box_rotated
    dst_points = np.float32([[0, 0], [0, desired_size[1]], [desired_size[0], 0], [desired_size[0], desired_size[1]]])
    warped_pcb2 = cv2.getPerspectiveTransform(src_points, dst_points)
    warped_pcb2 = cv2.warpPerspective(image, warped_pcb2, desired_size)
    return warped_pcb2

            