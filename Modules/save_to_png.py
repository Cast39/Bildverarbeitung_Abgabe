import cv2
import os


def saveToPNG( image, folder_path, file_name, 
    file_name_appendix="edited", overwrite=True ):
    
    # Synthezise file path
    output_file_name = (
        os.path.splitext(file_name)[0] + "_" + file_name_appendix + ".png"
    )
    output_path = os.path.join(folder_path, output_file_name)
    # try writing it
    if not (os.path.exists(folder_path)):  # unless folder doesn't exist
        return (-1, "path doesn't exist")
    if os.path.exists(output_path) and overwrite == False:  # unless filename exists
        return (-1, "file exists already")

    try:
        cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
        cv2.imwrite(output_path, image)
        return (0, output_path)
    except cv2.error:
        return (-1, "couldn't parse image to .PNG")
