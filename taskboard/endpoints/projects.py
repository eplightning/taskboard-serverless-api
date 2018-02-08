from taskboard import app, helpers
from flask import jsonify, request, abort
from taskboard.models import Project, Sprint, User

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


