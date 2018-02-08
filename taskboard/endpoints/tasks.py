from taskboard import app, helpers
from flask import jsonify, request, abort
from taskboard.models import Project, Task, User

@app.route('/projects/<uuid:project>/tasks')
def get_tasks(project):
    project = helpers.require_project(project)
    tasks = Task.query(project.id)

    return jsonify([dict(x) for x in tasks])

@app.route('/projects/<uuid:project>/tasks/<uuid:id>')
def get_task(project, id):
    project = helpers.require_project(project)
    task = Task.get(project.id, str(id))
    
    return jsonify(dict(task))


