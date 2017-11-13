from flask import Flask
from flask import got_request_exception
import os
import rollbar
import rollbar.contrib.flask
import webob

app = Flask(__name__)

@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token for the demo app: https://rollbar.com/demo
        '',
        # environment name
        'flasktest_bana',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/details_file/<name>', methods=['GET'])
def get_details(name):
    try:
        info = os.stat(name)
        response = list()
        data = dict()
        data['st_mode'] = info.st_mode
        data['st_ino'] = info.st_ino
        data['st_dev'] = info.st_dev
        data['st_nlink'] = info.st_nlink
        response.append(data)
        return webob.Response(json=response, content_type='application/json')
    except Exception as e:
        return webob.Response(
            json=dict(message="Invalid request", details=e.strerror),
            status=400)

