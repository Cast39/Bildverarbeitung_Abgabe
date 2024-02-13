import os
import cv2
#own module
from Modules.get_contours import get_contours
from Modules.get_box import get_box
from Modules.align import align
from Modules.crop import crop
from Modules.orient import orient
from Modules.scale import scale


testdata = {"path":".\Test\in",
            "destination":".\Test\out",
            "images":[]}

def main():
    #init all pictures in /Test/in
    print(testdata["path"])
    for file in os.listdir(testdata["path"]):
        if file.lower().endswith((".jpg",".png",".tiff",".tif")):
            testdata["images"].append(cv2.imread(testdata["path"]+'\\'+file))
    print(testdata["images"][0][25,25])

    #test functions
    for image in testdata["images"]:
        contours = get_contours(image)
        cv2.fillPoly(image, contours, (0,0,255))
        cv2.imshow("Konturen",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



main()