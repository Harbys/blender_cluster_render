import flask
import logging
from device_utils import Config, Job, Que
import json


app = flask.Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
config = Config()
que = Que()


@app.after_request
def set_server_name(response):
    response.headers["server"] = "device_api_server"
    return response


@app.route('/add_to_work_que', methods=["POST"])
def add_job():
    data = json.loads(flask.request.json)
    que.add_job(Job(data['job_id'], data["file_name"], data["fstart"], data["fend"]))
    print(que)
    return ''


def run():
    app.run(port=config.port, host='0.0.0.0', threaded=True)
