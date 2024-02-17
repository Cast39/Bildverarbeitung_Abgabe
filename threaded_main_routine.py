from os import path, listdir, getcwd
from threading import Thread

# own module
from Modules.segment import segment
from Modules.get_contour import get_contour
from Modules.boundary_box import boundary_box
from Modules.align import align
from Modules.crop import crop
from Modules.orient import orient
from Modules.scale import scale
from Modules.save_to_png import saveToPNG
from Modules.load_as_png import loadAsPNG
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
    box, _, _, _ = boundary_box(get_contour(helperImg))  # 5+6
    # also possible instead of 5+6, maybe own module "merge"?
    # segmentiertesalignImage = seg.segmentierung(alignImage)
    # segmentiertesalignImage = cv2.bitwise_not(segmentiertesalignImage)

    align(image, center, angle, size)  # 7
    # DEBUG: cv2.drawContours(alignImage, [align_box], 0, (0, 255, 0, 255), 2), not for main_routine pls reffer to test_routine
    image = crop(image, box)  # 8
    orient(image)  # 9
    return scale(image)  # 10


### handle whole dataset
#VARS
THREADS = []
ALLOWED_THREADS = 4

CUR_DIR = getcwd()
INPUT_PATH = path.join(CUR_DIR, "Images\in")
OUTPUT_PATH = path.join(CUR_DIR, "Images\out\png-Images")


# define single file-handling:
def process_file(file_name):
    # load picture
    _, image = loadAsPNG(path.join(INPUT_PATH, file_name)) #error handling intentionally missing, due to lack of relevance

    # save picture
    saveToPNG(
        edit_image(image),
        OUTPUT_PATH,
        path.splitext(file_name)[0],
        overwrite=True,
    )


# process all files in multiple threads
file_list = listdir(INPUT_PATH)
for file_name in file_list:
    # Verarbeite nur Bilddateien (ignoriere nicht-Bild-Dateien)
    if file_name.endswith((".jpg", ".jpeg", ".JPG", ".png", ".bmp")):
        # set up threads
        while len(THREADS) >= ALLOWED_THREADS:
            THREADS[0].join()
            THREADS.pop(0)
        THREADS.append(Thread(target=process_file, args=(file_name,)))
        THREADS[len(THREADS)-1].start()

#wait for all to finish
while len(THREADS) > 0:
    THREADS[0].join()
    #DEBUG: print("joined", len(THREADS))
    THREADS.pop(0)

# Teile Bilder zufällig in Training- und Test-Datensätze
divide(
    OUTPUT_PATH,
    path.join(CUR_DIR, "Images\out\Train"),
    path.join(CUR_DIR, "Images\out\Test"),
)
print("Done.")