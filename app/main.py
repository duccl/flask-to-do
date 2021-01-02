from flask import Flask,request
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


if __name__ == "__main__":
    if os.environ.get("PRODUCTION"):
        app.run()
    else:
        app.run(debug=True)