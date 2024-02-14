import os
import cv2
import numpy as np

# own module
from Modules.remove_background import remove_background
from Modules.get_contours import get_contours
from Modules.get_biggest_contour import get_biggest_contour
from Modules.boundary_box import boundary_box
from Modules.align import align
from Modules.crop import crop
from Modules.orient import orient
from Modules.scale import scale
from Modules.save_to_png import saveToPNG


testdata = {
    "path": ".\\Test\\in",
    "destination": ".\\Test\\out",
    "images": [],
    "filename": [],
}


def main():
    # init all pictures in /Test/in
    print("reading from: " + testdata["path"])
    for file in os.listdir(testdata["path"]):
        if file.lower().endswith((".jpg", ".png", ".tiff", ".tif")):
            testdata["images"].append(cv2.imread(testdata["path"] + "\\" + file))
            testdata["filename"].append(file)
    # DEBUG:print(testdata["images"][0][25, 25])

    # test functions -DEBUG state rn, TODO: formal Tests
    # Test all images in testdata["path"] and saves them to source
    # After each processing step the image window updates, press any key to continue to next step
    i = 0
    for image in testdata["images"]:
        out = image.copy()
        # remove_background
        out = remove_background(image)
        cv2.imshow("out", out)
        cv2.setWindowTitle("out", "no background")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # get_contours(image) -> contours[]
        contours = get_contours(image)
        cv2.fillPoly(out, contours, (0, 0, 255))
        cv2.imshow("out", out)
        cv2.setWindowTitle("out", "all contours")
        cv2.waitKey(0)
        # get_biggest_contour(contours) -> contour
        contour = get_biggest_contour(contours)
        cv2.fillPoly(out, contour, (0, 255, 0))
        cv2.imshow("out", out)
        cv2.setWindowTitle("out", "biggest contour")
        cv2.waitKey(0)
        # boundarybox(contur, minSize) -> box[], center, angle
        box, center, size, angle = boundary_box(contour)
        cv2.polylines(out, [box], True, color=(255, 0, 0), thickness=4)
        cv2.imshow("out", out)
        cv2.setWindowTitle("out", "boundary found")
        cv2.waitKey(0)
        # align(image, center, angle) -> alignedimg
        alignedimg = align(image, center, angle, size)
        out = alignedimg.copy()
        out = cv2.polylines(out, [box], True, color=(255, 0, 0), thickness=4)
        cv2.imshow("out", out)
        cv2.setWindowTitle("out", "aligned")
        cv2.waitKey(0)
        # crop(alignedimg,fin_box[])
        out = crop(
            alignedimg, boundary_box(get_biggest_contour(get_contours(alignedimg)))[0]
        )
        # DEBUG: print(np.flip(out.shape[:2]))
        cv2.imshow("out", out)
        cv2.resizeWindow("out", np.flip(image.shape[:2]))
        cv2.setWindowTitle("out", "cropped")
        cv2.waitKey(0)
        # orient(alignedimg) -> orientedimg
        out = orient(out)
        cv2.imshow("out", out)
        cv2.setWindowTitle("out", "oriented")
        cv2.waitKey(0)
        # scale(orientedimg) -> finimg
        out = scale(out)
        cv2.imshow("out", out)
        cv2.setWindowTitle("out", "scaled")
        cv2.waitKey(0)
        # save_to_png
        _,state = saveToPNG(out, testdata["destination"] + "\\", testdata["filename"][i])
        cv2.setWindowTitle("out", state)
        i += 1
        cv2.waitKey(0)
        cv2.destroyAllWindows()


main()
