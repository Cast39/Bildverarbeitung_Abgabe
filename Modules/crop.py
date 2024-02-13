import numpy as np
import cv2


def crop(rotated_image,crop_width,crop_hight,box):
    
    desired_size = (box[3][0]-box[0][0], box[0][1]-box[1][1]) # breite und höhe
    # Konvertiere die Eckpunkte des Rechtecks in das richtige Format für die Transformation
    src_points = np.float32([[box[1][0],box[1][1]], [box[0][0],box[0][1]], [box[2][0],box[2][1]], [box[3][0],box[3][1]]])
    dst_points = np.float32([[box[1][0],box[1][1]], [box[0][0],box[0][1]], [box[2][0],box[2][1]], [box[3][0],box[3][1]]])
    warped_pcb2 = cv2.getPerspectiveTransform(src_points, dst_points)
    warped_pcb2 = cv2.warpPerspective(rotated_image, warped_pcb2, desired_size)
    return warped_pcb2

    