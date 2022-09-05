import abc
from re import A
from repository import models
from pydantic import UUID4
from aiofiles import os as aios
import aioredis
import aiofiles

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass 

    @abc.abstractmethod
    async def get(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self):
        raise NotImplementedError


    @abc.abstractmethod
    async def save(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self):
        raise NotImplementedError


class FileRepository(AbstractRepository):

    def __init__(self):
        pass

    async def save(self,file):
        async with aiofiles.open(file.filename,"wb+") as f:
            contents = await file.read()
            await f.write(contents)
    async def get(self):
        pass 

    async def update(self):
        pass

    async def delete(self,pathfilename):
        await aios.remove(pathfilename)



class FileInfoRepository(AbstractRepository):
    model = models.FileInfo


    def __init__(self,db_type,host,port,db_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.db_type = db_type 
        self.db = None
        
    async def delete(self):
        pass 

    async def save(self):
        pass

    async def update(self):
        pass

    async def get(self):
        pass

    def build_url(self):
        url = f"{self.db_type}://{self.host}:{self.port}/{self.db}"
        return url

    async def create_engine(self):
        pass

class RedisFileInfoRepository(FileInfoRepository):
    model = models.FileInfo

    def __init__(self,db_type,host,port,db_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.db_type = db_type 
        self.db = None
        
    async def delete(self, key):
        return await self.db.delete(key)

    async def save(self,key, value):
        await self.db.set(key,value)

    async def get(self, key):
        return await self.db.get(key)

    async def update(self, key, value):
        return await self.db.set(key, value)

    def build_url(self):
        url = f"{self.db_type}://{self.host}:{self.port}/{self.db}"
        return url

    async def create_engine(self):
        url = self.build_url()
        self.db = await aioredis.from_url(url)


