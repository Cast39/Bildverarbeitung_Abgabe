import numpy as np
import cv2
import os

def saveToPNG(image,folder_path,file_name):
    # TODO: OS-Handling (try, catch) TODO:Return value (maybe new filepath?)
    output_file_name = os.path.splitext(file_name)[0] + "_edited.png"
    output_path = os.path.join(folder_path, output_file_name)
    cv2.imwrite(output_path, image)