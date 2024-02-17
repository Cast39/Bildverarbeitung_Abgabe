from cv2 import cvtColor, imwrite, COLOR_RGBA2BGRA, error
from os import path


def saveToPNG( image, folder_path, file_name, 
    file_name_appendix="edited", overwrite=True ):
    
    # Synthezise file path
    output_file_name = (
        path.splitext(file_name)[0] + "_" + file_name_appendix + ".png"
    )
    output_path = path.join(folder_path, output_file_name)
    # try writing it
    if not (path.exists(folder_path)):  # unless folder doesn't exist
        return (-1, "path doesn't exist")
    if path.exists(output_path) and overwrite == False:  # unless filename exists
        return (-1, "file exists already")

    try:
        cvtColor(image, COLOR_RGBA2BGRA)
        imwrite(output_path, image)
        return (0, output_path)
    except error:
        return (-1, "couldn't parse image to .PNG")
