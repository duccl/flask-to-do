from uuid import uuid1
from typing import List

class BaseModel:
    def __init__(self):
        self.id = uuid1().hex
    
    def to_dict(self,projection:List[str] = None):
        if not projection:
            return self.__dict__
        data_to_dump = {}
        for field in projection:
            data_to_dump[field] = self.__dict__.get(field)
        return data_to_dump

class Task(BaseModel):
    def __init__(self,
                 task_name:str,
                 task_owner:str,
                 task_endpoint:str):
        super().__init__()
        self.task_name = task_name
        self.task_owner = task_owner
        self.status = "To do"
        self.link = f'{task_endpoint}/{self.id}'

    def __str__(self):
        return self.task_name