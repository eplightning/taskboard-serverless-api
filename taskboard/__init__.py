from flask import Flask
import logging

logging.basicConfig()
log = logging.getLogger("pynamodb")
log.setLevel(logging.DEBUG)
log.propagate = True

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,PUT')
    return response

import taskboard.endpoints.projects
import taskboard.endpoints.sprints
import taskboard.endpoints.tasks
import taskboard.endpoints.swimlanes
