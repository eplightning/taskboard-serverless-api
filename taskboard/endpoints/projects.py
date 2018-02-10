from taskboard import app, helpers
from flask import jsonify, request, abort
from taskboard.models import Project, Sprint, User
import uuid

@app.route('/projects')
def get_projects():
    try:
        user = User.get(helpers.get_user_email())
        available_projects = [] if user.projects is None else list(user.projects)
    except:
        available_projects = []

    return jsonify([dict(x) for x in Project.batch_get(available_projects)])

@app.route('/projects/<uuid:id>')
def get_project(id):
    project = helpers.require_project(id)
    
    return jsonify(dict(project))

@app.route('/projects', methods=['POST'])
def create_project():
    input = helpers.get_input()

    id = str(uuid.uuid4())
    members = list(input['members']) if 'members' in input and input['members'] is not None else []
    owner = helpers.get_user_email()
    name = input['name']

    all_members = members + [owner]
    existing = []

    for member in User.batch_get(all_members):
        existing.append(member.email)
        member.update(actions=[
            User.projects.add({id})
        ])

    with User.batch_write() as batch:
        for member in all_members:
            if member not in existing:
                batch.save(User(member, projects=[id]))

    project = Project(id, name=name, members=members, owner=owner)
    project.save()

    return jsonify(dict(project))

@app.route('/projects/<uuid:id>', methods=['PUT'])
def edit_project(id):
    project = helpers.require_project(id)
    id = str(id)
    input = helpers.get_input()

    members = list(input['members']) if 'members' in input and input['members'] is not None else []
    name = input['name']
    old_members = list(project.members) if project.members is not None else []
    removed_members = [x for x in old_members if x not in members]
    added_members = [x for x in members if x not in old_members]

    existing = []
    for member in User.batch_get(removed_members + added_members):
        existing.append(member.email)

        if member in removed_members:
            member.update(actions=[
                User.projects.delete({id})
            ])
        else:
            member.update(actions=[
                User.projects.add({id})
            ])
    
    with User.batch_write() as batch:
        for member in added_members:
            if member not in existing:
                batch.save(User(member, projects=[id]))
    
    project.name = name
    project.members = members
    project.save()

    return jsonify(dict(project))

@app.route('/projects/<uuid:id>', methods=['DELETE'])
def delete_project(id):
    project = helpers.require_project(id)
    id = str(id)

    old_members = list(project.members) if project.members is not None else []

    for member in User.batch_get(old_members + [project.owner]):
        member.update(actions=[
            User.projects.delete({id})
        ])

    project.delete()

    return '', 201
