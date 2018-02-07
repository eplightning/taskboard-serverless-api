from taskboard import app
from flask import jsonify
from taskboard.models import Project, Sprint

@app.route('/')
def funcname():
    items = [x.swimlanes[0].name for x in Sprint.scan()]
    return jsonify(items)

