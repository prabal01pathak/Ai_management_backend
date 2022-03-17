import os
import base64
from pathlib import Path


def get_list_of_files(directory):
    """
    Returns a list of all files in a directory
    :param directory:
    :return:
    """
    files = os.listdir(directory)
    # make directory of files
    file_dict = {}
    for i,file in enumerate(files):
        file_dict[i] = directory + "/" + file
    return file_dict

def convert_image_to_base64(image_path):
    """
    Converts an image to base64
    :param image_path:
    :return:
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string

