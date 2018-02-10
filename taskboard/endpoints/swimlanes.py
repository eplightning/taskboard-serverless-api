import uuid
from taskboard import app, helpers
from flask import jsonify, request, abort
from taskboard.models import Project, Sprint, User, Swimlane

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

@app.route('/projects/<uuid:project>/sprints/<uuid:sprint>/swimlanes', methods=['POST'])
def new_swimlane(project, sprint):
    project = helpers.require_project(project)
    sprint = Sprint.get(project.id, str(sprint))
    input = helpers.get_input()
    swimlanes = sprint.swimlanes if sprint.swimlanes is not None else []

    id = str(uuid.uuid4())
    description = input['description']
    name = input['name']
    points = input['points']

    swimlane = Swimlane(id=id, description=description, name=name, points=points)
    swimlanes.append(swimlane)

    sprint.swimlanes = swimlanes
    sprint.save()

    return jsonify(dict(swimlane))

@app.route('/projects/<uuid:project>/sprints/<uuid:sprint>/swimlanes/<uuid:id>', methods=['PUT'])
def edit_swimlane(project, sprint, id):
    project = helpers.require_project(project)
    sprint = Sprint.get(project.id, str(sprint))
    id = str(id)
    input = helpers.get_input()
    swimlanes = sprint.swimlanes if sprint.swimlanes is not None else []
    swimlane = next(x for x in swimlanes if x.id == id)

    description = input['description']
    name = input['name']
    points = input['points']

    swimlane.description = description
    swimlane.name = name
    swimlane.points = points

    sprint.swimlanes = swimlanes
    sprint.save()

    return jsonify(dict(swimlane))

@app.route('/projects/<uuid:project>/sprints/<uuid:sprint>/swimlanes/<uuid:id>', methods=['DELETE'])
def delete_swimlane(project, sprint, id):
    project = helpers.require_project(project)
    sprint = Sprint.get(project.id, str(sprint))
    id = str(id)
    swimlanes = sprint.swimlanes if sprint.swimlanes is not None else []
    swimlanes = [x for x in swimlanes if x.id != id]

    sprint.swimlanes = swimlanes
    sprint.save()

    return '', 201
