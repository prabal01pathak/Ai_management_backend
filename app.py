from fastapi import FastAPI, Request, WebSocket, UploadFile, File, Depends
# import jsonresponse
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
import os
import sys
import shutil
from sharepoint_utils.directory_utils import (
        get_list_of_files, 
        convert_image_to_base64, 
        make_annotations_path, 
        get_total_annotations_done,
        projects,
        check_annotations_exist,
    )
from authentication.auth_utils import router, get_current_user, get_current_active_user
from authentication.schema import User
#import sqlalchemy
#from database_utils.database import engine, db, Base
#from databases import Database
#from database_utils.models import user, extra


app = FastAPI()
application_home_dir = os.path.dirname(os.path.abspath(__file__))
path_of_images = os.path.join(application_home_dir, 'images')
images_dict = get_list_of_files(path_of_images)

app.include_router(router, prefix="/auth")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Process-Time"] = "0.123"
    return response

@app.get("/")
async def root(current_user: User = Depends(get_current_user)):
    return {"message": "Hello World"}

@app.get("/projects")
async def get_projects(current_user: User = Depends(get_current_user)):
    user = current_user.username
    data = {}
    for project in projects.keys():
        annotations_path = make_annotations_path(user, project)
        data[project] = {}
        data[project]["project_name"] = projects[project]
        data[project]["annotations_done"] = len(get_total_annotations_done(annotations_path))
        no_of_images = len(images_dict)
        data[project]["no_of_images"] =  no_of_images
    return data



@app.get("/images/{project_id}")
async def get_images(project_id, request: Request, current_user: User = Depends(get_current_user)):
    user = current_user.username
    annotations_path = make_annotations_path(user, project_id)
    total_annotations_done = get_total_annotations_done(annotations_path)
    print(total_annotations_done)
    return {"images": images_dict, "total_annotations_done": total_annotations_done}
    #return JSONResponse(images_dict)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json(images_dict)
    while True:
        data = await websocket.receive_text()
        print(data)
        #image_path = images_dict[int(data["file"])]
        await websocket.send("image_path")

@app.get("/images/{project_id}/{image_id}")
def image_file(
        project_id, 
        image_id,
        request: Request, 
        current_user: User = Depends(get_current_active_user)
    ):
    print(project_id)
    image = images_dict[int(image_id)]
    image = os.path.join(path_of_images, image)
    media_type = "image/jpeg"
    return FileResponse(image, media_type=media_type)

@app.get("/images/annotations/{project_id}/{annotation_file_id}")
def get_annotations(
        project_id, 
        annotation_file_id,
        request: Request, 
        current_user: User = Depends(get_current_active_user)
    ):
    user = current_user.username
    annotation_file_id = int(annotation_file_id)
    annotations_path = make_annotations_path(user, project_id)
    valid_annotations = check_annotations_exist(user, project_id, annotation_file_id)
    print(valid_annotations)
    if valid_annotations:
        # media type is files
        media_type = "application/files"
        return FileResponse(valid_annotations, media_type=media_type)

    else:
        return {"annotations": "No annotations found"}

@app.post("/images/annotations/{project_id}")
async def image_annotation_save(
        project_id, 
        request: Request, 
        file: UploadFile = File(...), 
        current_user: User = Depends(get_current_active_user)
    ):
    user = current_user.username
    project_id = int(project_id)
    user_annotation_path = os.path.join("annotations", user, projects[int(project_id)])
    file_path = os.path.join(user_annotation_path, file.filename)
    with open(file_path, 'wb') as f:
        shutil.copyfileobj(file.file, f)
    return JSONResponse({"message": "File saved"})


