from taskboard import app, helpers
from flask import jsonify, request, abort
from taskboard.models import Project, Sprint, User

@app.route('/projects/<uuid:project>/sprints')
def get_sprints(project):
    project = helpers.require_project(project)
    sprints = Sprint.query(project.id)

    return jsonify([dict(x) for x in sprints])

@app.route('/projects/<uuid:project>/sprints/<uuid:id>')
def get_sprint(project, id):
    project = helpers.require_project(project)
    sprint = Sprint.get(project.id, str(id))
    
    return jsonify(dict(sprint))


