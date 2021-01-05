from flask import Flask,request, make_response
from models import Task
import os
import json

app = Flask(__name__)
tasks = {}

@app.route("/task/list")
def list_tasks():
    return json.dumps(list(map(lambda _key: tasks.get(_key).to_json(),tasks)))

@app.route("/task/add",methods=["POST"])
def add_tasks():
    data = json.loads(request.data)
    new_task = Task(task_name=data.get("task_name"),task_owner=data.get("task_owner"))
    tasks[new_task.id] = new_task
    return new_task.to_json()

@app.route("/task/update",methods=["POST"])
def update_task():
    data = json.loads(request.data)
    task_to_update = tasks.get(data.get('id'))
    if task_to_update:
        task_to_update.status = data.get('status')
        tasks[task_to_update.id] = task_to_update
        return task_to_update.to_json(['id','status'])
    return make_response('NOT FOUND',404)

@app.route("/task/delete",methods=["POST"])
def delete_task():
    data = json.loads(request.data)
    task_to_remove = tasks.get(data.get('id'))
    if task_to_remove:
        del tasks[task_to_remove.id]
        return json.dumps({'removed':True})
    return make_response('NOT FOUND',404)


if __name__ == "__main__":
    if os.environ.get("PRODUCTION"):
        app.run()
    else:
        app.run(debug=True)