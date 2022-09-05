from repository.repositories import FileInfoRepository, FileRepository, RedisFileInfoRepository
from repository.config import REDIS_HOST,REDIS_PORT,REDIS_DB,REDIS_TYPE
import redis
import ujson
from repository import models

async def save_file(file):
    repo = FileRepository()
    await repo.save(file)

async def save_fileinfo_redis(id,path_filename,filename,extension):
    fileinfo = models.FileInfo(id,filename,extension,pathfilename=path_filename)
    repo = RedisFileInfoRepository(db_type=REDIS_TYPE,host=REDIS_HOST,port=REDIS_PORT,db_name=REDIS_DB)
    await repo.create_engine()
    key = fileinfo.id
    data_for_dump = fileinfo.to_json()
    value = ujson.dumps(data_for_dump)
    print(key)
    print(value)
    await repo.save(key, value)


async def get_fileinfo_redis(id):
    repo = RedisFileInfoRepository(db_type=REDIS_TYPE,host=REDIS_HOST,port=REDIS_PORT,db_name=REDIS_DB)
    await repo.create_engine()
    fileinfo = await repo.get(id)
    return fileinfo
    
async def update_fileinfo_redis_start_processing(id,fileinfo:dict):
    repo = RedisFileInfoRepository(db_type=REDIS_TYPE,host=REDIS_HOST,port=REDIS_PORT,db_name=REDIS_DB)
    await repo.create_engine()
    fileinfo["processing"] = True
    fileinfo["processingProgress"] = 0
    await repo.update(id,fileinfo)

    

async def delete_fileinfo_redis(id):
    repo = RedisFileInfoRepository(db_type=REDIS_TYPE,host=REDIS_HOST,port=REDIS_PORT,db_name=REDIS_DB)
    filerepo = FileRepository()
    await repo.create_engine()
    fileinfo = await repo.get(id)
    print(fileinfo)
    if fileinfo is None:
        return False
    else:
        load_data = ujson.loads(fileinfo)
        filename = load_data["pathfilename"]
        await repo.delete(id)
        await filerepo.delete(filename)
        return True
        
def update_fileinfo_processing_ready(id):
    r = redis.Redis(host=REDIS_HOST,port=REDIS_PORT,db_name=REDIS_DB)
    r.set(id)
    # repo = RedisFileInfoRepository(db_type=REDIS_TYPE,host=REDIS_HOST,port=REDIS_PORT,db_name=REDIS_DB)
    # await repo.create_engine()
    # fileinfo["processing"] = True
    # fileinfo["processingProgress"] = 0
    # await repo.update(id,fileinfo)