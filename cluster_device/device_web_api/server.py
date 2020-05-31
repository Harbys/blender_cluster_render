import flask
import logging
from device_utils import Config, Job, Que, Executor
import json

# create a new flask app
app = flask.Flask(__name__)
# disable print log for cleaner console
log = logging.getLogger('werkzeug')
log.disabled = True
# config to be used by server and executor
config = Config()
# work queue
que = Que()
# work executor
executor = Executor(que, config)


# change the default header
@app.after_request
def set_server_name(response):
    response.headers["server"] = "device_api_server"
    return response


# used to add new jobs to the queue
@app.route('/add_to_work_que', methods=["POST"])
def add_job():
    # data verification needs to be added here
    data = json.loads(flask.request.json)
    # a new jobs is added
    que.add_job(Job(data['job_id'], data["file_name"], data["fstart"], data["fend"], data["blend_file"]))
    return flask.make_response({
        "action": "job_added"
    })


def run():
    app.run(port=config.port, host='0.0.0.0', threaded=True)
