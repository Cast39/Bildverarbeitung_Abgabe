import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# own module
from Modules.segment import segment
from Modules.remove_background import remove_background
from Modules.get_contour import get_contour
from Modules.get_kontur_graph import get_kontur_graph
from Modules.align import align
from Modules.crop import crop
from Modules.orient import orient
from Modules.scale import scale
from Modules.save_to_png import saveToPNG
from Modules.load_as_png import loadAsPNG


TESTDATA = {
    "path": ".\\Test\\in",
    "destination": ".\\Test\\out",
    "images": [],
    "filenames": [],
}


def main():
    # init all pictures in /Test/in
    print("reading from: " + TESTDATA["path"])
    for file in os.listdir(TESTDATA["path"]):
        if file.lower().endswith((".jpg", ".png", ".tiff", ".tif")):
            TESTDATA["images"].append(loadAsPNG(TESTDATA["path"] + "\\" + file)[1]) #error handling intentionally missing, due to lack of relevance
            TESTDATA["filenames"].append(file)
    # DEBUG:print(TESTDATA["images"][0][25, 25])

    # test functions -DEBUG state rn, TODO: formal Tests, if possible
    # Test all images in TESTDATA["path"] and saves them to destination
    # After each processing step the image window updates, press any key to continue to next step
    i = 0
    for image in TESTDATA["images"]:
        # pls ignore helper fn
        def show(msg):
            cv2.imshow("out", out)
            cv2.setWindowTitle("out", msg)
            if cv2.waitKey(0) == ord("s"):
                _, state = saveToPNG(
                    out,
                    TESTDATA["destination"] + "\\",
                    TESTDATA["filenames"][i],
                    msg,
                    True,
                )
                cv2.setWindowTitle("out", state)
                cv2.waitKey(0)

        ###init
        out = np.copy(image)
        show(TESTDATA["filenames"][i])

        # implement your sequence here,
        # every image stored in var out will be displayed by fn show()
        # press any key to move on after show() and 's'-key to save currently displayed image
        ### flow under test:

        # segment(image) -> transparentimg
        segment(image)
        out = image.copy()
        #show("segmented")

        # TODO: more precise alternative to segment
        # remove_background(image, rey, +-15)
        # out = remove_background(image)
        # show("nobckgrnd")

        # get_contour(transparentimage) -> contour
        contour = get_contour(image)
        cv2.fillPoly(out, contour, (0, 0, 255, 255))
        #show("contour")

        # boundary_box(contur) -> box[], center, angle
        #box, center, size, angle = boundary_box(contour)
        konturverlauf = np.array(get_kontur_graph(contour))
        #cv2.polylines(out, [box], True, color=(255, 0, 0, 255), thickness=4)
        
        plt.plot(konturverlauf[:,0], konturverlauf[:,1]) # x=winkel y=radius
        plt.show()
        plt.plot(konturverlauf[:,0], konturverlauf[:,2]) # x=winkel y=radius
        plt.show()
        return
        show("boundary")

        # align(image, center, angle) -> alignedimg
        align(image, center, angle, size)
        out = image.copy()
        out = cv2.polylines(out, [box], True, color=(255, 0, 0, 255), thickness=4)
        show("aligned")

        # crop(alignedimg,fin_box[])
        image = crop(image, boundary_box(get_contour(image))[0])
        out = image.copy()
        # DEBUG: print(np.flip(out.shape[:2]))
        show("cropped")

        # orient(alignedimg) -> orientedimg
        orient(image)
        out = image.copy()
        show("oriented")

        # scale(orientedimg) -> finimg
        image = scale(image)
        out = image.copy()
        show("scaled")

        # save_to_png
        _, state = saveToPNG(
            image,
            TESTDATA["destination"] + "\\",
            TESTDATA["filenames"][i],
            overwrite=False,
        )
        show(state)

        ### pls ignore
        i += 1
        cv2.destroyAllWindows()


main()
