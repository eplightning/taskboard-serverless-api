from flask import Flask
import logging

logging.basicConfig()
log = logging.getLogger("pynamodb")
log.setLevel(logging.DEBUG)
log.propagate = True

app = Flask(__name__)

import taskboard.endpoints.projects
import taskboard.endpoints.sprints
import taskboard.endpoints.tasks
import taskboard.endpoints.swimlanes
