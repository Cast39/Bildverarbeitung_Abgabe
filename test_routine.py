import os
import cv2
import numpy as np

# own module
from Modules.segmentierung import segmentierung
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
            testdata["images"].append(
                cv2.cvtColor(
                    cv2.imread(testdata["path"] + "\\" + file), cv2.COLOR_RGB2RGBA
                )
            )
            testdata["filename"].append(file)
    # DEBUG:print(testdata["images"][0][25, 25])

    # test functions -DEBUG state rn, TODO: formal Tests
    # Test all images in testdata["path"] and saves them to source
    # After each processing step the image window updates, press any key to continue to next step
    i = 0
    for image in testdata["images"]:
        # helper
        def show(msg):
            cv2.imshow("out", out)
            cv2.setWindowTitle("out", msg)
            if cv2.waitKey(0) == ord("s"):
                _, state = saveToPNG(
                    out, testdata["destination"] + "\\", testdata["filename"][i], msg
                )
                cv2.setWindowTitle("out", state)
                cv2.waitKey(0)

        ###init
        out = image.copy()
        show(testdata["filename"][i])
        ###flow
        # segementierung(image)
        out = segmentierung(image)
        show("no background")
        # get_contours(image) -> contours[]
        contours = get_contours(image)
        cv2.fillPoly(out, contours, (0, 0, 255))
        show("contours")
        # get_biggest_contour(contours) -> contour
        contour = get_biggest_contour(contours)
        cv2.fillPoly(out, contour, (0, 255, 0))
        show("biggest contour")
        # boundary_box(contur, minSize) -> box[], center, angle
        box, center, size, angle = boundary_box(contour)
        cv2.polylines(out, [box], True, color=(255, 0, 0), thickness=4)
        show("boundary")
        # align(image, center, angle) -> alignedimg
        alignedimg = align(image, center, angle, size)
        out = alignedimg.copy()
        out = cv2.polylines(out, [box], True, color=(255, 0, 0), thickness=4)
        show("aligned")
        # crop(alignedimg,fin_box[])
        out = crop(
            alignedimg, boundary_box(get_biggest_contour(get_contours(alignedimg)))[0]
        )
        # DEBUG: print(np.flip(out.shape[:2]))
        show("cropped")
        # orient(alignedimg) -> orientedimg
        out = orient(out)
        show("oriented")
        # scale(orientedimg) -> finimg
        out = scale(out)
        show("scaled")
        # save_to_png
        _, state = saveToPNG(
            out, testdata["destination"] + "\\", testdata["filename"][i]
        )
        i += 1
        show(state)
        cv2.destroyAllWindows()


main()
