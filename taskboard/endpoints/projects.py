from taskboard import app, helpers
from flask import jsonify, request, abort
from taskboard.models import Project, Sprint, User
import uuid

@app.route('/projects')
def get_projects():
    try:
        user = User.get(helpers.get_user_email())
        available_projects = list(user.projects) if user.projects is not None else []
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
    members = set(input['members'])
    owner = helpers.get_user_email()
    name = input['name']

    all_members = members | {owner}
    existing = set()

    for member in User.batch_get(all_members):
        existing.add(member.email)
        member.update(actions=[
            User.projects.add({id})
        ])

    with User.batch_write() as batch:
        for member in all_members - existing:
            batch.save(User(member, projects=[id]))

    project = Project(id, name=name, members=members, owner=owner)
    project.save()

    return jsonify(dict(project))

@app.route('/projects/<uuid:id>', methods=['PUT'])
def edit_project(id):
    project = helpers.require_project(id)
    id = str(id)
    input = helpers.get_input()

    members = set(input['members'])
    name = input['name']
    old_members = set(project.members) if project.members is not None else set()
    removed_members = old_members - members
    added_members = members - old_members

    existing = set()
    for member in User.batch_get(removed_members | added_members):
        existing.add(member.email)

        if member in removed_members:
            member.update(actions=[
                User.projects.delete({id})
            ])
        else:
            member.update(actions=[
                User.projects.add({id})
            ])
    
    with User.batch_write() as batch:
        for member in added_members - existing:
            batch.save(User(member, projects=[id]))
    
    project.name = name
    project.members = members
    project.save()

    return jsonify(dict(project))

@app.route('/projects/<uuid:id>', methods=['DELETE'])
def delete_project(id):
    project = helpers.require_project(id)
    id = str(id)

    old_members = set(project.members) if project.members is not None else set()

    for member in User.batch_get(old_members | {project.owner}):
        member.update(actions=[
            User.projects.delete({id})
        ])

    project.delete()

    return '', 201
