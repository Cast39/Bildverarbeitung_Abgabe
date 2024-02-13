import os
import cv2
#own module
import Modules.get_contours as get_contours
import Modules.align as align
import Modules.crop as crop
import Modules.orient as orient
import Modules.scale as scale

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
        print(contours)



main()