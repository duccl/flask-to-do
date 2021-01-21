from flask import Flask
from flask.helpers import make_response
from flask_restful import Api,Resource,request
from flask_login import LoginManager,login_required, login_user, current_user
import os
from models import User,Task
import time

app = Flask(__name__)
login = LoginManager(app)
api = Api(app)
app.secret_key = os.environ.get('SECRET_KEY')
VERSION = os.environ.get('TASK_API_VERSION') if os.environ.get('TASK_API_VERSION') else 'v1'


@login.user_loader
def load_user(id):
    return User.get_by_id(id)

class UsersController(Resource):
    model = User

    def post(self):
        data = request.get_json()
        if 'password' not in data:
            make_response(400,'Password not informed!')
        user = self.model(name=data.get('name'),password=data.get('password'))
        user.save()
        return user.to_dict(['name','id'])

class UserController(Resource):
    model = UsersController.model
    def retrieve_user(self,uuid) -> User:
        _object = self.model.get_by_id(uuid)
        assert _object
        return _object

    def post(self,uuid):
        data = request.get_json()
        user = self.retrieve_user(uuid)
        if user.is_password_valid(data.get('password')):
            login_user(user)
            return user.to_dict(['id','name','tasks'])
        make_response(403,'Access denied')

class TasksController(Resource):
    model = Task

    @login_required
    def post(self):
        new_task = Task(title=request.get_json().get("title"),
                    owner=current_user,
                    owner_id = current_user.id,
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

    @login_required
    def delete(self,uuid):
        self.model.delete(uuid)
        return {'removed':True}

    @login_required
    def put(self,uuid):
        task_to_update = self.retrieve_task(uuid)
        task_to_update.update(request.get_json())
        return task_to_update.to_dict()

    def get(self,uuid):
        return self.retrieve_task(uuid).to_dict()

api.add_resource(UserController,f'/api/{VERSION}/user/login/<string:uuid>')
api.add_resource(UsersController,f'/api/{VERSION}/users')
api.add_resource(TaskController,f'/api/{VERSION}/task/<string:uuid>')
api.add_resource(TasksController,f'/api/{VERSION}/tasks')


if __name__ == "__main__":
    if os.environ.get("PRODUCTION"):
        app.run(host=os.environ.get('FLASK_HOST'))
    else:
        app.run(debug=True)
        