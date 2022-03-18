from fastapi import FastAPI, Request, WebSocket, UploadFile, File, Depends
# import jsonresponse
from fastapi.responses import JSONResponse, StreamingResponse
import os
import sys
import shutil
from directory_utils import get_list_of_files, convert_image_to_base64
from authentication.auth_utils import router, get_current_user
from authentication.schema import User
#import sqlalchemy
#from database_utils.database import engine, db, Base
#from databases import Database
#from database_utils.models import user, extra

app = FastAPI()
images_dict = get_list_of_files("C:/users/hp/pictures")

app.include_router(router, prefix="/auth")

@app.get("/")
async def root(current_user: User = Depends(get_current_user)):
    return {"message": "Hello World"}

@app.get("/images")
async def get_images(request: Request, current_user: User = Depends(get_current_user)):
    # set images_dict to request.state
    request.state.images_dict = images_dict
    return JSONResponse(images_dict)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json(images_dict)
    while True:
        data = await websocket.receive_text()
        print(data)
        #image_path = images_dict[int(data["file"])]
        await websocket.send("image_path")

@app.get("/images/{id}")
def image_file(
        id, 
        request: Request, 
        current_user: User = Depends(get_current_user)
    ):
    image = images_dict[int(id)]
    image = os.path.join("C:/users/hp/pictures", image)
    return StreamingResponse(open(image, 'rb'), media_type='image/jpeg')

@app.post("/images/annotation/{id}")
async def image_annotation_save(
        id, 
        request: Request, 
        file: UploadFile = File(...), 
        current_user: User = Depends(get_current_user)
    ):
    # save file to disk
    file_path = "C:/users/hp/pictures/annotation/" + file.filename
    with open(file_path, 'wb') as f:
        shutil.copyfileobj(file.file, f)

