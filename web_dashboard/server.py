import flask
import logging
import cluster_utils
import login_manager

# web server used for both user dashboard and api for device communication
app = flask.Flask(__name__)

# disables logging to avoid cluttered console output
log = logging.getLogger('werkzeug')
log.disabled = True

# config used by both web dashboard and cluster controller
config = cluster_utils.Config()

# cluster controller
cluster = cluster_utils.Cluster(config)

# login manager, used for user authentication
with open("web_dashboard/user_db/users.json") as userfile:
    lm = login_manager.LoginManager(userfile)


# changes default server header for security reasons
@app.after_request
def set_server_name(response):
    response.headers["server"] = "cluster_web_dash"
    return response


# defines index page
@app.route("/", methods=['GET'])
def index():
    # automatic redirect of already logged in users
    # authenticated by a cookie
    try:
        token = flask.request.cookies["sessionid"]
        if lm.is_logged_in(token):
            return flask.redirect("/dashboard")
    # if cookie doesn't exist it throws KeyError
    except KeyError:
        pass
    return flask.render_template('index.html')


# defines login page
@app.route("/login", methods=["GET", "POST"])
def login_page():
    # request get results in response with redirect to index page
    if flask.request.method == "GET":
        return flask.redirect("/")

    # form data is verified by login manager
    if lm.verify(flask.request.form["login"], flask.request.form["password"]):
        # make response and set appropriate cookie with token
        resp = flask.make_response(flask.redirect("/dashboard"))
        token = lm.make_token()
        # tell login manager to bind token to username for later authentication
        lm.login(flask.request.form["login"], token)
        resp.set_cookie('sessionid', token)
        return resp
    else:
        # if login and/or password are wrong return to index page with #wrong_credentials to display a message
        return flask.redirect("/#wrong_credentials")


# checks if logged in, and if so returns /dashboard website, if not redirects to index
@app.route("/dashboard")
def dashboard():
    # if cookie sessionid doesn't exist, redirects do index
    try:
        token = flask.request.cookies["sessionid"]
        if lm.is_logged_in(token):
            return flask.render_template("dashboard.html")
        else:
            return flask.redirect("/")
    except KeyError:
        return flask.redirect("/")


# returns json with all devices
@app.route("/get_devices")
def get_devices():
    try:
        token = flask.request.cookies["sessionid"]
        if lm.is_logged_in(token):
            devices = {}
            for device_elem in cluster.devices:
                devices[device_elem.hwid] = {
                    "hwid": device_elem.hwid,
                    "ip_addr": device_elem.ipaddr,
                    "port": device_elem.port,
                    "performance": device_elem.performance
                }
            return devices
        else:
            return "Not authenticated"
    except KeyError:
        return "Not authenticated"


@app.route('/add_device')
def add_device():
    try:
        token = flask.request.cookies["sessionid"]
        if not lm.is_logged_in(token):
            return "Not authenticated"
    except KeyError:
        return "Not authenticated"

    return flask.render_template('add_device.html')


# returns site with device info
@app.route('/device/<device_id>')
def device(device_id):
    try:
        token = flask.request.cookies["sessionid"]
        if lm.is_logged_in(token):
            try:
                # pass device to template
                dev = cluster.find_device_by_hwid(device_id)
                dev = {
                    "hwid": dev.hwid,
                    "ip_addr": dev.ipaddr,
                    "port": dev.port,
                    "performance": dev.performance
                }
                return flask.render_template("device.html", device=dev)
            except KeyError:
                return flask.redirect("/dashboard")
        else:
            return "Not authenticated"
    except KeyError:
        return "Not authenticated"


# expects form to edit device
@app.route('/edit_device', methods=["POST"])
def edit_device():
    try:
        token = flask.request.cookies["sessionid"]
        if lm.is_logged_in(token):
            # data needs to be verified here | to be added
            # note to future, don't just pass data to edit function
            data = flask.request.form
            cluster.edit_device(data)
            return "Success"
        else:
            return "Not authenticated"
    except KeyError:
        return "Not authenticated"


# used for communication between cluster devices
# this one is received when a device has finished its part of a job
@app.route("/dev_api", methods=["POST"])
def dev_api():
    data = flask.request.form
    # delete id of a device from wait list of specified job
    # used for detecting when are jobs finished
    cluster.delete_waiting_for(data["job"], data["hwid"])
    return "done"


def run():
    app.run(host='0.0.0.0', port=config.port, threaded=True)
