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
    try:
        token = flask.request.cookies["sessionid"]
        if lm.is_logged_in(token):
            return flask.redirect("/dashboard")
    except KeyError:
        pass
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
        return flask.redirect("/#wrong_credentials")


@app.route("/dev_api", methods=["POST"])
def dev_api():
    data = flask.request.form
    cluster.delete_waiting_for(data["job"], data["hwid"])
    return "done"


@app.route("/dashboard")
def dashboard():
    token = flask.request.cookies["sessionid"]
    if lm.is_logged_in(token):
        return flask.render_template("dashboard.html")
    else:
        return flask.redirect("/")


@app.route("/get_devices")
def get_devices():
    try:
        token = flask.request.cookies["sessionid"]
        if not lm.is_logged_in(token):
            return "Not authenticated"
    except KeyError:
        return "Not authenticated"
    devices = {}
    for device in cluster.devices:
        devices[device.hwid] = {
            "hwid": device.hwid,
            "ip_addr": device.ipaddr,
            "port": device.port,
            "performance": device.performance
        }
    return devices


@app.route('/device/<device_id>')
def device(device_id):
    try:
        token = flask.request.cookies["sessionid"]
        if not lm.is_logged_in(token):
            return "Not authenticated"
    except KeyError:
        return "Not authenticated"

    try:
        dev = cluster.find_device_by_hwid(device_id)
        return str(dev.port)
    except KeyError:
        return "No such device"


def run():
    app.run(host='0.0.0.0', port=2452, threaded=True)
