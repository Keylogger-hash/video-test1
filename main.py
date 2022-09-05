from fastapi import FastAPI, File,UploadFile
from repository.config import VIDEOS_DIR
import os 
import aioredis
import ujson
import uuid
from validation_models.base_models import FileResizeFormat
from video_processing_tasks.processing_tasks import processing_video_resize
from repository.services import save_fileinfo_redis,save_file, get_fileinfo_redis,delete_fileinfo_redis

app = FastAPI()


@app.get("/")
async def healthy():
    return {"status":"OK","status_code":200}


@app.post("/file")
async def upload_file(file: UploadFile = File(...)):
    r = await aioredis.from_url('redis://localhost:6379/0')
    if not file:
        return {"error":"No file uploaded"}
    else:
        uuid4 = str(uuid.uuid4())
        extension = file.content_type.split("/")[1]
        filename = f"{str(uuid4)}.{extension}"
        path_filename = os.path.join(VIDEOS_DIR,filename)
        file.filename = path_filename
        await save_fileinfo_redis(uuid4,path_filename,filename,extension)
        await save_file(file)
        return {"id":uuid4}

@app.patch("/file/{id}")
async def processing_file(id: str,format:FileResizeFormat):
    fileinfo = await get_fileinfo_redis(id)
    if fileinfo is None:
        return {"success":False,"error":f"{id} video not found"}
    else:
        file_data = ujson.loads(fileinfo)
        width = format.width
        height = format.height
        processing_video_resize.delay(id,file_data,width,height)
        return {"success":True}

@app.get("/{id}")
async def get_fileinfo(id: str):
    fileinfo = await get_fileinfo_redis(id)
    if fileinfo is None:
        return {"success":False,"error":f"{id} video not found"}
    else:
        json_fileinfo = ujson.loads(fileinfo)
        data = {"id":id,"fileinfo":json_fileinfo}
        return {"success":True,"data":data}


@app.delete("/delete/{id}")
async def delete_file(id:str):
    success = await delete_fileinfo_redis(id)
    return {"success":success}