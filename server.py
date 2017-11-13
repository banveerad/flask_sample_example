from flask import Flask
import os
import rollbar
import webob

rollbar.init('')
app = Flask(__name__)

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
        rollbar.report_message('File name: %s %s' % (name, e.strerror))
        return webob.Response(
            json=dict(message="Invalid request", details=e.strerror),
            status=400)

