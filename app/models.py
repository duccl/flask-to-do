from uuid import uuid1
from json import dumps
from typing import List

class BaseModel:
    def __init__(self):
        self.id = uuid1().hex
    
    def to_json(self,projection:List[str] = None):
        if not projection:
            return dumps(self.__dict__)
        data_to_dump_as_json = {}
        for field in projection:
            data_to_dump_as_json[field] = self.__dict__.get(field)
        return dumps(data_to_dump_as_json)

class Task(BaseModel):
    status = "To do"
    def __init__(self,
                 task_name:str,
                 task_owner:str):
        super().__init__()
        self.task_name = task_name
        self.task_owner = task_owner

    def close_task(self):
        self.status = "Done"
    
    def doing_task(self):
        self.status = "Doing"

    def __str__(self):
        return self.task_name