import cv2
import os

# own module
from Modules.segment import segment
from Modules.get_contour import get_contour
from Modules.boundary_box import boundary_box
from Modules.align import align
from Modules.crop import crop
from Modules.orient import orient
from Modules.scale import scale
from Modules.save_to_png import saveToPNG
from Modules.divide import divide

# Feel free to test within test_routine.py
# only then replace the following with a better sequence if found
### define algorithm:
# 1. segment(image) -> transparentimg
# 2. get_contour(transparentimg) -> contour
# 3. boundary_box(contour) -> 'box[], center, size, angle

# 4. align(transparentimg, center, angle) -> altransimg
# *5. get_contour(altransimg) -> fin_contour                *can be replaced by enhancable function module "merge"
# *6. boundary_box(fin_contur) -> fin_box[], 'center, 'angle

# 7. align(image, center, angle) -> alignedimg             <- !origimg! for conserving background
# 8. crop(alignedimg,fin_box[]) -> croppedimg
# 9. orient(croppedimg) -> orientedimg
# 10. scale(orientedimg) -> final_img

# (11. save_to_png(final_img))


### implementation of algorithm:
def edit_image(image):
    helperImg = segment(image.copy())  # 1
    _, center, size, angle = boundary_box(get_contour(helperImg))  # 2+3

    align(helperImg, center, angle, size)  # 4
    box,_,_,_ = boundary_box(get_contour(helperImg))  # 5+6
    # also possible instead of 5+6, maybe own module "merge"?
    # segmentiertesalignImage = seg.segmentierung(alignImage)
    # segmentiertesalignImage = cv2.bitwise_not(segmentiertesalignImage)

    align(image, center, angle, size)  # 7
    # DEBUG: cv2.drawContours(alignImage, [align_box], 0, (0, 255, 0, 255), 2), not for main_routine pls reffer to test_routine
    image = crop(image, box)  # 8
    orient(image)  # 9
    return scale(image)  # 10

### handle whole dataset

# Aktuelles Arbeitsverzeichnis festlegen
current_directory = os.getcwd()
folder_path = os.path.join(current_directory, "Images\in")

# Iteriere über jede Datei im Ordner
file_list = os.listdir(folder_path)
for file_name in file_list:

    # Verarbeite nur Bilddateien (ignoriere nicht-Bild-Dateien)
    if file_name.endswith((".jpg", ".jpeg", ".JPG", ".png", ".bmp")):
        # Bildpfad konkatenieren
        image_path = os.path.join(folder_path, file_name)

        # Bild laden, .PNG konform
        image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_RGB2RGBA)

        # Speichere das bearbeitete Bild als PNG-Datei
        output_file_name = os.path.splitext(file_name)[0]
        output_path = os.path.join(folder_path, output_file_name)

        saveToPNG(
            edit_image(image),
            os.path.join(current_directory, "Images\out\png-Images"),
            output_file_name,
            overwrite=True,
        )

# Teile Bilder zufällig in Training- und Test-Datensätze
divide(
    os.path.join(current_directory, "Images\out\png-Images"),
    os.path.join(current_directory, "Images\out\Train"),
    os.path.join(current_directory, "Images\out\Test"),
)
print("Done.")


#############archive##############

# image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\anomaly_011.JPG")
# #image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\anomaly_012.JPG")
# #image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\normal_0000.JPG")
# #image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\normal_0015.JPG")
# #image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\normal_0029.JPG")

# image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\0003.JPG")
# image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\0010.JPG")
# image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\025.JPG")
# image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\035.JPG")
# image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\053.JPG")
# image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\095.JPG")
# image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\0297.JPG")
# image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\0360.JPG")
# image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\0383.JPG")

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