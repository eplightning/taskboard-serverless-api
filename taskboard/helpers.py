from taskboard.models import Project
from flask import abort, request

def get_user_email():
    return 'wrexdot@gmail.com'

def require_project(id):
    id = str(id)
    project = Project.get(id)
    email = get_user_email()

    if project.owner != email and (project.members is None or email not in project.members):
        abort(403)
    
    return project

def get_input():
    if not request.is_json:
        abort(400)

    return request.get_json()
