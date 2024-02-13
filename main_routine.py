#get_contours(image) -> contours[]
#get_Box(conturs, minSize) -> box[], center, angle
#align(image, center, angle) -> alignedimg
#getcontours(alignedimg) -> fin_contours[]
#get_Box(fin_conturs, minSize) -> fin_box[], center, angle
#crop(alignedimg,fin_box[])
#orient -TODO

import Modules.align as ali
import Modules.crop as cr
import Modules.divide as div
import Modules.get_biggest_contour as bigcon
import Modules.get_box as get_box
import Modules.get_contours as con
import Modules.orient as ori
import Modules.save_to_png as save
import Modules.scale as scale
import cv2


image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\anomaly_011.JPG")
#image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\anomaly_012.JPG")
#image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\normal_0000.JPG")
#image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\normal_0015.JPG")
#image = cv2.imread(r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\normal_0029.JPG")

biggest_contour = bigcon.get_biggest_contour(con.get_contours(image))
box, center,size, angle = get_box.get_box(biggest_contour)

alignImage = ali.align(image,center, angle, size)
biggest_align_contour = bigcon.get_biggest_contour(con.get_contours(alignImage))
align_box, align_center, aligh_size, align_angle = get_box.get_box(biggest_align_contour)
cv2.drawContours(alignImage, [align_box], 0, (0, 255, 0), 2)
cropImage = cr.crop(alignImage,align_box)
scaleImage = scale.scale(cropImage)
save.saveToPNG(scaleImage,r"C:\Users\49152\Desktop\Bildverarbeitung_Abgabe\Images\Train","anomaly_011")

#image_height, image_width = scaleImage.shape[:2]
#print("Bildgröße (Breite x Höhe):", image_width, "x", image_height, "Pixel")

cv2.imshow("Image with box", scaleImage)
cv2.waitKey(0)
cv2.destroyAllWindows()