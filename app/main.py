from flask import Flask,request, make_response
from models import Task
from utils import URLS,TASK_ROOT
import os
import json

app = Flask(__name__)
tasks = {}

@app.route(URLS.get('list_task'))
def list_tasks():
    return json.dumps(list(map(lambda _key: tasks.get(_key).__dict__,tasks)))

@app.route(URLS.get('add_task'),methods=["POST"])
def add_tasks():
    data = json.loads(request.data)
    new_task = Task(task_name=data.get("task_name"),
                    task_owner=data.get("task_owner"),
                    task_endpoint=TASK_ROOT)
    tasks[new_task.id] = new_task
    return new_task.to_json()

@app.route(URLS.get('get_task'))
def get_task(uuid):
    task = tasks.get(uuid)
    if task:
        return task.to_json()
    return make_response('NOT FOUND',404)

@app.route(URLS.get('update_task'),methods=["POST"])
def update_task():
    data = json.loads(request.data)
    task_to_update = tasks.get(data.get('id'))
    if task_to_update:
        task_to_update.status = data.get('status')
        tasks[task_to_update.id] = task_to_update
        return task_to_update.to_json(['id','status'])
    return make_response('NOT FOUND',404)

@app.route(URLS.get('delete_task'),methods=["POST"])
def delete_task():
    data = json.loads(request.data)
    task_to_remove = tasks.get(data.get('id'))
    if task_to_remove:
        del tasks[task_to_remove.id]
        return json.dumps({'removed':True})
    return make_response('NOT FOUND',404)


if __name__ == "__main__":
    if os.environ.get("PRODUCTION"):
        app.run(host=os.environ.get('FLASK_HOST'))
    else:
        app.run(debug=True)