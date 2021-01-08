from flask import Flask
from flask_restful import Api,Resource,request
from models import Task
import os

app = Flask(__name__)
api = Api(app)
VERSION = os.environ.get('TASK_API_VERSION') if os.environ.get('TASK_API_VERSION') else 'v1.0'

class TasksController(Resource):
    model = {}
    def post(self):
        new_task = Task(task_name=request.get_json().get("task_name"),
                    task_owner=request.get_json().get("task_owner"),
                    task_endpoint=request.path[:-1])
        self.model[new_task.id] = new_task
        return new_task.to_dict()
    
    def get(self):
        return list(map(lambda _key: self.model.get(_key).to_dict(),self.model))


class TaskController(Resource):
    model = TasksController.model
    def retrieve_task(self,uuid) -> Task:
        _object = self.model.get(uuid)
        assert _object
        return _object
        
    def delete(self,uuid):
        task_to_delete = self.retrieve_task(uuid)
        del self.model[task_to_delete.id]
        return {'removed':True}

    def put(self,uuid):
        task_to_update = self.retrieve_task(uuid)
        task_to_update.status = request.get_json().get('status')
        self.model[task_to_update.id] = task_to_update 
        return task_to_update.to_dict(['id','status','link'])

    def get(self,uuid):
        return self.retrieve_task(uuid).to_dict()

api.add_resource(TaskController,f'/api/{VERSION}/task/<string:uuid>')
api.add_resource(TasksController,f'/api/{VERSION}/tasks')

if __name__ == "__main__":
    if os.environ.get("PRODUCTION"):
        app.run(host=os.environ.get('FLASK_HOST'))
    else:
        app.run(debug=True)