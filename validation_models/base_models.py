from lib2to3.pytree import Base
from pydantic import BaseModel, conint




class FileResizeFormat(BaseModel):
    width: conint(gt=20) 
    height: conint(gt=20)