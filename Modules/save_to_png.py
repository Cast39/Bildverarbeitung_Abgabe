import cv2
import os


def saveToPNG(image, folder_path, file_name):
    #Synthezise file path
    output_file_name = os.path.splitext(file_name)[0] + "_edited.png"
    output_path = os.path.join(folder_path, output_file_name)
    #try writing it
    if not(os.path.exists(folder_path)): return (-1,"path dosn't exist")
    try:
        cv2.imwrite(output_path, image)
        return (0,output_path)
    except cv2.error:
        return (-1,"couldn't parse image to .PNG")
