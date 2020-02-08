import flask
import logging
from device_utils import Config, Job


app = flask.Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
config = Config()


@app.after_request
def set_server_name(response):
    response.headers["server"] = "cluster_web_dash"
    return response


@app.route('/add_to_work_que', methods=["POST"])
def add_job():
    print(flask.request.form["fstart"])
    return ''


def run():
    app.run(port=config.port, host='0.0.0.0', threaded=True)