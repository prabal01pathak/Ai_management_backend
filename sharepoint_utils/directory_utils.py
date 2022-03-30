import os
import base64
from pathlib import Path
import zipfile
import io
from fastapi.responses import StreamingResponse
from shareplum import Site
from shareplum import Office365
from shareplum.site import Version


email= os.environ['EMAIL']
password = os.environ["PASSWORD"]
site = "ML_team-BioconPoc/"

authcookie = Office365(f'https://resoluteaisoftware.sharepoint.com', username=email, password=password).GetCookies()

site = Site(f'https://resoluteaisoftware.sharepoint.com/sites/{site}', version=Version.v365, authcookie=authcookie)
#fake data

projects = {
    1: "NLP",
    2: "ML",
    3: "AI",
    4: "Deep Learning",
    5: "New Project",
    6: "#3rd Project",
    7: "#4th Project",
    8: "#5th Project",
    9: "#6th Project",
}
#=======

base_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/').split('/')[:-1]
home_dir = os.path.join(*base_dir)
# go one directory up

def get_list_of_files(directory: str) -> dict:
    """
    Returns a list of all files in a directory
    :param directory:
    :return:
    """
    print(directory)
    files = os.listdir(directory)
    # make directory of files
    file_dict = {}
    for i,file in enumerate(files):
        file_dict[i] = file
    return file_dict

def convert_image_to_base64(image_path: str) -> str:
    """
    Converts an image to base64
    :param image_path:
    :return:
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string


def make_annotations_path(username: str ,project_id: int) -> str:
    """
    Creates the path to the annotations file
    :param username:
    :param project_id:
    :return: path
    """
    annotations_path = os.path.join(home_dir,'annotations',username)
    if not os.path.exists(annotations_path):
        os.makedirs(annotations_path)
        print('annotations directory created')
    print(annotations_path)
    annotations_path = os.path.join(annotations_path,projects[int(project_id)])
    print(annotations_path)
    if not os.path.exists(annotations_path):
        os.makedirs(annotations_path)
    return annotations_path

def get_total_annotations_done(annotations_path: str) -> dict:
    files = get_list_of_files(annotations_path)
    return files

def check_annotations_exist(user: str ,project_id: int, annotation_id: int):
    application_home_dir = home_dir
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

