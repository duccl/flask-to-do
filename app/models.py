from typing import Any, List, Dict
from uuid import uuid1
from sqlalchemy import Column,CheckConstraint,String,ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
import database_context as database

class BaseModel:
    __table_args__ = {'extend_existing': True}
    id = None

    def init_id_if_necessary(function):
        def wrapps(self,*args,**kwargs):
            if not self.id:
                self.id = uuid1().hex
            function(self,*args,**kwargs)
        return wrapps
    
    def project_attribute(self, name: str) -> Any:
        if callable(self.__dict__.get(name)) or name.startswith('_'):
            return None
        elif hasattr(self.__dict__.get(name),'to_dict'):
            return name,self.__dict__.get(name).to_dict()
        return name,self.__dict__.get(name) 

    def to_dict(self,projection:List[str]=None):
        if projection:
            return dict(map(lambda project: (project,self.__dict__.get(project)),projection))
        return dict(
            filter(
                lambda _projected_value: _projected_value != None,
                map(
                    lambda attribute: self.project_attribute(attribute),
                    self.__dict__
                )
            )   
        )

    @classmethod
    def get_by_id(cls,id):
        session = database.Session()
        return session.query(cls).get(id)

    @classmethod
    def delete(cls,id):
        session = database.Session()
        session.query(cls).filter(cls.id == id).delete()
        session.commit()

    @classmethod
    def get_all(cls):
        session = database.Session()
        return session.query(cls).all()

    @init_id_if_necessary
    def save(self):
        session = database.Session()
        session.add(self)
        session.commit()

    @init_id_if_necessary
    def update(self, attributes_to_change:Dict[str,str]):
        session = database.Session()
        for key in attributes_to_change:
            self.__setattr__(key,attributes_to_change[key])
        session.commit()

    def __str__(self):
        return self.id

    init_id_if_necessary = staticmethod(init_id_if_necessary)

class User(UserMixin,database.Base,BaseModel):
    __tablename__ = 'tblUsers'
    id = Column(String(200),primary_key=True)
    name = Column(String(200),nullable=False)
    password = Column(String(256),nullable=False)
    tasks = relationship('Task',cascade='all, delete')

    def __init__(self,**kwargs) -> None:
        super().__init__(**kwargs)
        self.password = generate_password_hash(self.password,method='sha256')

    def is_password_valid(self,password):
        return check_password_hash(self.password,password)

    def __str__(self) -> str:
        return self.name

class Task(database.Base,BaseModel):
    __tablename__ = 'tblTasks'
    id = Column(String(200),primary_key=True)
    title = Column(String(200),nullable=False)
    link = Column(String(200))
    status = Column(String(30))
    owner_id = Column(String(200),ForeignKey('tblUsers.id',ondelete='CASCADE'))
    owner = relationship('User',
            back_populates='tasks')
    
    CheckConstraint("status = 'Doing' or status = 'Done' or status = 'To Do'",
                    name='status_CheckConstraint')

    def __init__(self,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.status = "To Do"
        self.create_link_to_self()

    @BaseModel.init_id_if_necessary
    def create_link_to_self(self):
        if self.link:
            self.link += f'/{self.id}'

    def update(self, attributes_to_change: Dict[str, str]):
        if 'status' in attributes_to_change:
            super().update({'status':attributes_to_change['status']})

    def __str__(self):
        return self.title  

database.Base.metadata.create_all(bind=database.engine)