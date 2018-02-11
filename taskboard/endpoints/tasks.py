import uuid
from taskboard import app, helpers
from flask import jsonify, request, abort
from taskboard.models import Project, Task, User, Sprint, Swimlane

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

@app.route('/projects/<uuid:project>/tasks', methods=['POST'])
def new_task(project):
    project = helpers.require_project(project)
    input = helpers.get_input()

    sprint = Sprint.get(project.id, input['sprint_id'])

    id = str(uuid.uuid4())

    data = {
        'sprint_id': sprint.id,
        'swimlane_id': input['swimlane_id'],
        'state': input['state'],
        'name': input['name'],
        'description': input['description'] if input['description'] != '' else None,
        'planned_points': input['planned_points'],
        'points': input['points'],
        'assigned_members': set(input['assigned_members']) & project.all_members()
    }

    task = Task(project.id, id, **data)
    task.save()

    return jsonify(dict(task))

@app.route('/projects/<uuid:project>/tasks/<uuid:id>', methods=['PUT'])
def edit_task(project, id):
    project = helpers.require_project(project)
    task = Task.get(project.id, str(id))
    input = helpers.get_input()

    # sprint = Sprint.get(project, input['sprint_id'])

    data = {
        # 'sprint_id': sprint.id,
        # 'swimlane_id': input['swimlane_id'],
        'state': input['state'],
        'name': input['name'],
        'description': input['description'] if input['description'] != '' else None,
        'planned_points': input['planned_points'],
        'points': input['points'],
        'assigned_members': set(input['assigned_members']) & project.all_members()
    }

    for k, v in data.items():
        setattr(task, k, v)

    task.save()

    return jsonify(dict(task))

@app.route('/projects/<uuid:project>/tasks/<uuid:id>/position', methods=['PUT'])
def edit_task_position(project, id):
    project = helpers.require_project(project)
    task = Task.get(project.id, str(id))
    # state, swimlane_id, 
    input = helpers.get_input()

    task.swimlane_id = input['swimlane_id']

    # assign member when moving from new to any other state and there are no assigned members
    if task.state == 'new' and input['state'] != 'new' and not task.assigned_members:
        task.assigned_members = {helpers.get_user_email()}
    
    # clear points if moving to done
    if input['state'] == 'done':
        task.points = 0
    
    task.state = input['state']
    task.save()

    return jsonify(dict(task))

@app.route('/projects/<uuid:project>/tasks/<uuid:id>/points', methods=['PUT'])
def edit_task_points(project, id):
    project = helpers.require_project(project)
    task = Task.get(project.id, str(id))
    # points
    input = helpers.get_input()

    task.points = input['points']
    task.save()

    return jsonify(dict(task))

@app.route('/projects/<uuid:project>/tasks/<uuid:id>', methods=['DELETE'])
def delete_task(project, id):
    project = helpers.require_project(project)
    task = Task.get(project.id, str(id))

    task.delete()

    return '', 201
