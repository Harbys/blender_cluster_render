import flask
import logging
import cluster_utils
import login_manager

app = flask.Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
config = cluster_utils.Config()
cluster = cluster_utils.Cluster(config)
with open("web_dashboard/user_db/users.json") as userfile:
    lm = login_manager.LoginManager(userfile)


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
    if lm.verify(flask.request.form["login"], flask.request.form["password"]):
        resp = flask.make_response(flask.redirect("/dashboard"))
        token = lm.make_token()
        lm.login(flask.request.form["login"], token)
        resp.set_cookie('sessionid', token)
        return resp
    else:
        return 'wrong creds'


@app.route("/dev_api", methods=["POST"])
def dev_api():
    data = flask.request.form
    cluster.delete_waiting_for(data["job"], data["hwid"])
    return "done"


def run():
    app.run(host='0.0.0.0', port=2452, threaded=True)
