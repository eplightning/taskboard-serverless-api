from taskboard import app, helpers
from flask import jsonify, request, abort
from taskboard.models import Project, Sprint, User

@app.route('/projects/<uuid:project>/sprints/<uuid:sprint>/swimlanes')
def get_swimlanes(project, sprint):
    project = helpers.require_project(project)
    sprint = Sprint.get(project.id, str(sprint))
    swimlanes = sprint.swimlanes if sprint.swimlanes is not None else []

    return jsonify([dict(x) for x in swimlanes])

@app.route('/projects/<uuid:project>/sprints/<uuid:sprint>/swimlanes/<uuid:id>')
def get_swimlane(project, sprint, id):
    id = str(id)
    project = helpers.require_project(project)
    sprint = Sprint.get(project.id, str(sprint))
    swimlanes = sprint.swimlanes if sprint.swimlanes is not None else []
    swimlane = next(x for x in swimlanes if x.id == id)
    
    return jsonify(dict(swimlane))


