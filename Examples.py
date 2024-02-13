import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.svm import SVC

def run(image, result, settings):
    height, width, channels = image.shape[:]

    # Konvertiere das Bild in Graustufen
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarisierung des Bildes (zur Segmentierung)
    _, binary = cv2.threshold(gray, 134, 255, cv2.THRESH_BINARY)

    # Finde Konturen im binarisierten Bild
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Minimale Größe der Kontur
    min_contour_size = 26000



    # Iteriere über alle gefundenen Konturen
    for contour in contours:
        # Berechne die Fläche der Kontur
        area = cv2.contourArea(contour)
        
        # Überprüfe, ob die Fläche größer als die Mindestkonturgröße ist
        if area > min_contour_size:
            # Kopie des Originalbildes erstellen
            image_copy = image.copy()
            
            
            # Berechne das umschließende Rechteck für die geglättete Kontur
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            center, size, angle = rect
            cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
            



            # Rotiere das Bild um den Winkel
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=1)
            rotated_image = cv2.warpAffine(image_copy, rotation_matrix, (image_copy.shape[1], image_copy.shape[0]))
        
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
            desired_size = (980, 565)  # Beispielgröße, anpassen nach Bedarf
            # Konvertiere die Eckpunkte des Rechtecks in das richtige Format für die Transformation
            src_points = np.float32([[box_rotated[1][0],box_rotated[1][1]], [box_rotated[0][0],box_rotated[0][1]], [box_rotated[2][0],box_rotated[2][1]], [box_rotated[3][0],box_rotated[3][1]]])#box_rotated
            dst_points = np.float32([[0, 0], [0, desired_size[1]], [desired_size[0], 0], [desired_size[0], desired_size[1]]])
            warped_pcb2 = cv2.getPerspectiveTransform(src_points, dst_points)
            warped_pcb2 = cv2.warpPerspective(rotated_image, warped_pcb2, desired_size)

            
    result.append({"name": "pcb2", "data": warped_pcb2})

        


if __name__ == '__main__':
    image = cv2.imread("Images\Objekte.png")
    result = []
    run(image, result)
    for ele in result:
        cv2.imshow(ele["name"], ele["data"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

