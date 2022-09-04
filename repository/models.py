import dataclasses
from pydantic import UUID4

@dataclasses.dataclass
class FileInfo:
    id: str
    filename: str 
    extension: str
    pathfilename: str 
    processing: bool = False
    processingProgress: int  = 0

    def to_json(self):
        return {"filename":self.filename,"extension":self.extension,"pathfilename":self.pathfilename,"processing":self.processing,"processingProgress":self.processingProgress}

