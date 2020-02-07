import flask
import logging
import cluster_utils

app = flask.Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
config = cluster_utils.Config()


@app.after_request
def set_server_name(response):
    response.headers["server"] = "cluster_web_dash"
    return response


@app.route("/", methods=['GET'])
def index():
    return flask.render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if flask.request.method == "GET":
        return flask.redirect("/")
    return 'login'


def run():
    cluster = cluster_utils.Cluster()
    app.run(host='0.0.0.0', port=2452, threaded=True)
