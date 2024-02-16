import os
import cv2
import numpy as np

# own module
from Modules.segment import segment
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
    "filenames": [],
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
            testdata["filenames"].append(file)
    # DEBUG:print(testdata["images"][0][25, 25])

    # test functions -DEBUG state rn, TODO: formal Tests, if possible
    # Test all images in testdata["path"] and saves them to destination
    # After each processing step the image window updates, press any key to continue to next step
    i = 0
    for image in testdata["images"]:
        # pls ignore helper fn
        def show(msg):
            cv2.imshow("out", out)
            cv2.setWindowTitle("out", msg)
            if cv2.waitKey(0) == ord("s"):
                _, state = saveToPNG(
                    out,
                    testdata["destination"] + "\\",
                    testdata["filenames"][i],
                    msg,
                    True,
                )
                cv2.setWindowTitle("out", state)
                cv2.waitKey(0)

        ###init
        out = np.copy(image)
        show(testdata["filenames"][i])

# implement your sequence here, 
# every image stored in var out will be displayed by fn show()
# press any key to move on after show() and 's'-key to save currently displayed image
        ### flow under test:

        # segment(image) -> transparentimg
        image = segment(image)
        out = image.copy()
        show("segmented")

        # TODO: more precise alternative to segment
        # remove_background(image, rey, +-15)
        # out = remove_background(image)
        # show("nobckgrnd")

        # get_contours(transparentimage) -> contours[]
        contours = get_contours(image)
        cv2.fillPoly(out, contours, (0, 0, 255, 255))
        show("contours")

        # get_biggest_contour(contours[]) -> contour
        contour = get_biggest_contour(contours)
        cv2.fillPoly(out, contour, (0, 255, 0, 255))
        show("biggest contour")

        # boundary_box(contur) -> box[], center, angle
        box, center, size, angle = boundary_box(contour)
        cv2.polylines(out, [box], True, color=(255, 0, 0, 255), thickness=4)
        show("boundary")

        # align(image, center, angle) -> alignedimg
        image = align(image, center, angle, size)
        out = image.copy()
        out = cv2.polylines(out, [box], True, color=(255, 0, 0, 255), thickness=4)
        show("aligned")

        # crop(alignedimg,fin_box[])
        image = crop(image, boundary_box(get_biggest_contour(get_contours(image)))[0])
        out = image.copy()
        # DEBUG: print(np.flip(out.shape[:2]))
        show("cropped")

        # orient(alignedimg) -> orientedimg
        image = orient(image)
        out = image.copy()
        show("oriented")

        # scale(orientedimg) -> finimg
        image = scale(image)
        out = image.copy()
        show("scaled")

        # save_to_png
        _, state = saveToPNG(
            image,
            testdata["destination"] + "\\",
            testdata["filenames"][i],
            overwrite=False,
        )
        show(state)

        ### pls ignore
        i += 1
        cv2.destroyAllWindows()

main()
