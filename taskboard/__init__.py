from flask import Flask

app = Flask(__name__)

import taskboard.endpoints.projects
import taskboard.endpoints.sprints
import taskboard.endpoints.tasks
import taskboard.endpoints.swimlanes
