import os
import base64
from pathlib import Path
import zipfile
import io
from fastapi.responses import StreamingResponse

#fake data
projects = {
    1: "NLP",
    2: "ML",
    3: "AI",
    4: "Deep Learning",
    5: "New Project",
    6: "#3rd Project",
    7: "#4th Project",
}
#=======


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
        file_dict[i] = file
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


def make_annotations_path(username,project_id):
    annotations_path = os.path.join(os.getcwd(),'annotations',username)
    if not os.path.exists(annotations_path):
        os.makedirs(annotations_path)
        print('annotations directory created')
    print(annotations_path)
    annotations_path = os.path.join(annotations_path,projects[int(project_id)])
    print(annotations_path)
    if not os.path.exists(annotations_path):
        os.makedirs(annotations_path)
    return annotations_path

def get_total_annotations_done(annotations_path):
    files = get_list_of_files(annotations_path)
    return files

def check_annotations_exist(user,project_id,annotation_id):
    application_home_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(application_home_dir,'annotations',user,projects[int(project_id)])
    annotations = get_total_annotations_done(path).keys()
    if annotation_id in annotations:
        file_name = get_list_of_files(path)[annotation_id]
        return os.path.join(path,file_name)
    else:
        return False

def convert_to_zip(path1,path2, username, project_id):
    """
    Converts a directory to a zip file
    :param path1:
    :param path2:
    :return:
    print(zip_file_name)
    with zipfile.ZipFile(zip_file_name, 'w') as myzip:
        myzip.write(path1, os.path.basename(path1))
        myzip.write(path2, os.path.basename(path2))
    print('zip file created', zip_file_name)
    return zip_file_name
    """
    application_home_dir = os.path.dirname(os.path.abspath(__file__))
    print(application_home_dir)
    zip_file_name = os.path.join(application_home_dir,'annotations',username,projects[int(project_id)],username+'_'+projects[int(project_id)]+'.zip')
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, mode='w') as zf:
        zf.write(path1, os.path.basename(path1))
        zf.write(path2, os.path.basename(path2))
    return StreamingResponse(stream, media_type='application/zip', headers={'Content-Disposition': 'attachment; filename=%s' % zip_file_name})

