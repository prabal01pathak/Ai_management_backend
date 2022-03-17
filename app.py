from fastapi import FastAPI, Request, WebSocket, UploadFile, File
# import jsonresponse
from fastapi.responses import JSONResponse, StreamingResponse
import os
import sys
import shutil
from directory_utils import get_list_of_files, convert_image_to_base64

app = FastAPI()

images_dict = get_list_of_files("C:/users/hp/pictures")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/images")
async def get_images(request: Request):
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
def image_file(id, request: Request):
    image = images_dict[int(id)]
    return StreamingResponse(open(image, 'rb'), media_type='image/jpeg')

@app.post("/images/annotation/{id}")
async def image_annotation_save(id, request: Request, file: UploadFile = File(...)):
    # save file to disk
    file_path = "C:/users/hp/pictures/annotation/" + file.filename
    with open(file_path, 'wb') as f:
        shutil.copyfileobj(file.file, f)

