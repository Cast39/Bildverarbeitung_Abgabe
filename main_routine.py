#remove_background(image)
#get_contours(image) -> contours[]
#get_biggest_contour(contours) -> contour
#boundary_box(contour, minSize) -> box[], center, size, angle
#align(image, center, angle) -> alignedimg
#getcontours(alignedimg) -> fin_contours[]
#boundary_box(fin_conturs, minSize) -> fin_box[], center, angle
#crop(alignedimg,fin_box[])
#orient(alignedimg) -> orientedimg
#scale
#save_to_png

import Modules.align as ali
import Modules.crop as cr
import Modules.divide as div
import Modules.get_biggest_contour as bigcon
import Modules.boundary_box as bbox
import Modules.get_contours as con
import Modules.orient as ori
import Modules.save_to_png as save
import Modules.scale as scale
import Modules.sigmentierung as sig
import cv2
import os

# Aktuelles Arbeitsverzeichnis festlegen
current_directory = os.getcwd()

# Ordnerpfad mit den Bildern
folder_path = os.path.join(current_directory,"Images\src")

# Liste aller Dateien im Ordner
file_list = os.listdir(folder_path)

# Iteriere über jede Datei im Ordner
for file_name in file_list:
    # Verarbeite nur Bilddateien (ignoriere nicht-Bild-Dateien)
    if file_name.endswith(('.jpg', '.jpeg', '.JPG', '.png', '.bmp')):
        # Bildpfad erstellen
        image_path = os.path.join(folder_path, file_name)

        # Bild laden
        image = cv2.imread(image_path)

        sigmentiertesImage = sig.sigmentierung(image)
        biggest_contour = bigcon.get_biggest_contour(con.get_contours(sigmentiertesImage))
        box, center,size, angle = bbox.boundary_box(biggest_contour)

        alignImage = ali.align(image,center, angle, size)
        sigmentiertesalignImage = sig.sigmentierung(alignImage)
        sigmentiertesalignImage = cv2.bitwise_not(sigmentiertesalignImage)
        
        biggest_align_contour = bigcon.get_biggest_contour(con.get_contours(sigmentiertesalignImage))
        align_box, align_center, aligh_size, align_angle = bbox.boundary_box(biggest_align_contour)
        cv2.drawContours(alignImage, [align_box], 0, (0, 255, 0), 2)
        cropImage = cr.crop(alignImage,align_box)
        scaleImage = scale.scale(cropImage)

        # Speichere das bearbeitete Bild als PNG-Datei
        output_file_name = os.path.splitext(file_name)[0]
        output_path = os.path.join(folder_path, output_file_name)

        save.saveToPNG(scaleImage,os.path.join(current_directory,"Images\png_images"),output_file_name)

div.divide(os.path.join(current_directory,"Images\png_images"), os.path.join(current_directory,"Images\out\Train"), os.path.join(current_directory,"Images\out\Test"))
print("Done.")





# image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\anomaly_011.JPG")
# #image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\anomaly_012.JPG")
# #image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\normal_0000.JPG")
# #image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\normal_0015.JPG")
# #image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\normal_0029.JPG")

#image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\0003.JPG")
#image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\0010.JPG")
#image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\025.JPG")
#image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\035.JPG")
#image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\053.JPG")
#image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\095.JPG")
#image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\0297.JPG")
#image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\0360.JPG")
#image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\0383.JPG")

# biggest_contour = bigcon.get_biggest_contour(con.get_contours(image))
# box, center,size, angle = bbox.boundary_box(biggest_contour)

# alignImage = ali.align(image,center, angle, size)
# biggest_align_contour = bigcon.get_biggest_contour(con.get_contours(alignImage))
# align_box, align_center, aligh_size, align_angle = bbox.boundary_box(biggest_align_contour)
# cv2.drawContours(alignImage, [align_box], 0, (0, 255, 0), 2)
# cropImage = cr.crop(alignImage,align_box)
# scaleImage = scale.scale(cropImage)
# #save.saveToPNG(scaleImage,r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\Train","anomaly_011")

# #image_height, image_width = scaleImage.shape[:2]
# #print("Bildgröße (Breite x Höhe):", image_width, "x", image_height, "Pixel")

# cv2.imshow("Image with box", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()