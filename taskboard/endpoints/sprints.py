import uuid
import datetime
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

@app.route('/projects/<uuid:project>/sprints', methods=['POST'])
def new_sprint(project):
    project = helpers.require_project(project)
    input = helpers.get_input()

    id = str(uuid.uuid4())
    start_date = datetime.datetime.strptime(input['start_date'], '%Y-%m-%d')
    end_date = datetime.datetime.strptime(input['end_date'], '%Y-%m-%d')
    name = input['name']

    sprint = Sprint(project, id, start_date=start_date, end_date=end_date, name=name)
    sprint.save()

    return jsonify(dict(sprint))

@app.route('/projects/<uuid:project>/sprints/<uuid:id>', methods=['PUT'])
def edit_sprint(project, id):
    project = helpers.require_project(project)
    sprint = Sprint.get(project.id, str(id))
    input = helpers.get_input()

    start_date = datetime.datetime.strptime(input['start_date'], '%Y-%m-%d')
    end_date = datetime.datetime.strptime(input['end_date'], '%Y-%m-%d')
    name = input['name']

    sprint.name = name
    sprint.start_date = start_date
    sprint.end_date = end_date
    sprint.save()

    return jsonify(dict(sprint))

@app.route('/projects/<uuid:project>/sprints/<uuid:id>', methods=['DELETE'])
def delete_sprint(project, id):
    project = helpers.require_project(project)
    sprint = Sprint.get(project.id, str(id))

    sprint.delete()

    return '', 201
