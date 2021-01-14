from flask import Flask
from flask_restful import Api,Resource,request
import os
from models import User,Task
import time

app = Flask(__name__)
api = Api(app)
VERSION = os.environ.get('TASK_API_VERSION') if os.environ.get('TASK_API_VERSION') else 'v1.0'

class UsersController(Resource):
    model = User
    def retrieve_user(self,uuid) -> Task:
        _object = self.model.get_by_id(uuid)
        assert _object
        return _object

    def post(self):
        user = self.model(name=request.get_json().get('name'))
        user.save()
        return user.to_dict()

class UserController(Resource):
    model = UsersController.model
    def retrieve_user(self,uuid) -> User:
        _object = self.model.get_by_id(uuid)
        assert _object
        return _object

    def get(self,uuid):
        return self.retrieve_user(uuid).to_dict()

class TasksController(Resource):
    model = Task
    def post(self):
        owner = UsersController.model.get_by_id(request.get_json().get("owner_id"))
        new_task = Task(title=request.get_json().get("title"),
                    owner=owner,
                    owner_id = owner,
                    link=request.path[:-1])
        new_task.save()
        return new_task.to_dict()
    
    def get(self):
        return {'data':list(
            map(
                lambda record: record.to_dict(),
                self.model.get_all()       
            )
        )}


class TaskController(Resource):
    model = TasksController.model
    def retrieve_task(self,uuid) -> Task:
        _object = self.model.get_by_id(uuid)
        assert _object
        return _object
        
    def delete(self,uuid):
        self.model.delete(uuid)
        return {'removed':True}

    def put(self,uuid):
        task_to_update = self.retrieve_task(uuid)
        return task_to_update

    def get(self,uuid):
        return self.retrieve_task(uuid)

api.add_resource(UserController,f'/api/{VERSION}/user/<string:uuid>')
api.add_resource(UsersController,f'/api/{VERSION}/users')
api.add_resource(TaskController,f'/api/{VERSION}/task/<string:uuid>')
api.add_resource(TasksController,f'/api/{VERSION}/tasks')

if __name__ == "__main__":
    if os.environ.get("PRODUCTION"):
        app.run(host=os.environ.get('FLASK_HOST'))
    else:
        app.run(debug=True)
        