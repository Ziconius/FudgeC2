import time
import uuid

from flask import Flask, render_template, flash, request, jsonify, g, url_for, redirect, send_file  # ,make_response, session, current_app,
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_socketio import SocketIO

from Implant.Implant import ImplantSingleton
from ServerApp.modules.UserManagement import UserManagementController
from ServerApp.modules.StagerGeneration import StagerGeneration
from ServerApp.modules.ImplantManagement import ImplantManagement
from ServerApp.modules.ApplicationManager import AppManager
from ServerApp.modules.ExportManager import CampaignExportManager

Imp = ImplantSingleton.instance
UsrMgmt = UserManagementController()
ImpMgmt = ImplantManagement()
StagerGen = StagerGeneration()
AppManager = AppManager()
ExpoManager = CampaignExportManager()

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())
login = LoginManager(app)
login.init_app(app)
socketio = SocketIO(app)

# TODO: Controller dev work.
listener_management = None


# -- Context Processors --#
@app.context_processor
def inject_dict_for_all_auth_templates():
    # -- Returns the list of Campaigns the authenticated user has at least read access to
    if current_user.is_authenticated:
        return dict(campaignlist=UsrMgmt.campaign_get_user_campaign_list(current_user.user_email))
    else:
        return dict()


@app.context_processor
def inject_dict_for_all_campaign_templates():
    if 'cid' in g:
        cid = g.get('cid')
        campaign_name = AppManager.campaign_get_campaign_name_from_cid(cid)
        if cid is not None:
            return dict(campaign=campaign_name, cid=cid)
    return dict()


# -- Managing the error and user object. -- #
# ----------------------------------------- #
@login.user_loader
def load_user(user):
    return UsrMgmt.get_user_object(user)


@app.before_request
def before_request():
    return


@app.after_request
def add_header(r):
    return r


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('BaseHomePage'), 302)  # This should be a proper 404?


@app.errorhandler(401)
def page_not_found(e):
    return redirect(url_for('login'), 302)


# -- Authentication endpoints -- #
# ------------------------------ #
@app.route("/auth/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if 'email' in request.form and 'password' in request.form and request.form['email'] is not None and request.form['password'] is not None:
            UserObject = UsrMgmt.user_login(request.form['email'],request.form['password'])
            if UserObject is False:
                return redirect(url_for("BaseHomePage", error="Incorrect Username/Password"))

            if UserObject.first_logon == 1:
                login_user(UserObject)
                return redirect(url_for("BaseHomePage"))

            else:
                guid = UsrMgmt.get_first_logon_guid(request.form['email'])
                # return render_template("auth/PasswordResetPage.html",guid=guid)
                return redirect(url_for("PasswordReset", guid=guid))
    return render_template("auth/LoginPage.html", fudge_version=AppManager.get_software_verision_number(), fudge_version_name=AppManager.get_software_verision_name())


@app.route("/auth/logout")
@login_required
def logout():
    if (current_user.is_authenticated):
        logout_user()
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


@app.route("/auth/passwordreset", methods=['GET', 'POST'])
def PasswordReset():
    if request.method == "POST":
        print("In reset: {}".format(request.form))
        UserObject = UsrMgmt.change_password_first_logon(request.form)
        if UserObject is not False:
            login_user(UserObject)
            return redirect(url_for('BaseHomePage'))
    if request.method == "GET":
        print(request.args)
        guid = "0000-0000-0000-0000"
        if request.args.get('guid') is not None:

            print("We're now embedding: {}".format( request.args.get('guid')))
            guid = request.args.get('guid')
        return render_template("auth/PasswordResetPage.html", guid=guid)
    return redirect(url_for('login'))


# -- Main endpoints -- #
# -------------------- #
@app.route("/", methods=["GET", "POST"])
@login_required
def BaseHomePage():
    if request.method == "GET":
        return render_template("Homepage.html",
                               out_of_date=AppManager.check_software_version(),
                               version_number=AppManager.get_software_verision_number())
    elif request.method == "POST":
        return jsonify(AppManager.get_all_user_campaigns(current_user.user_email))


@app.route("/CreateCampaign", methods=['GET', 'POST'])
@login_required
def create_new_campaign():
    if request.method == "POST":
        success_bool, success_msg = AppManager.campaign_create_campaign(current_user.user_email, request.form)
        if success_bool is True:
            return redirect(url_for('BaseHomePage'))
        else:
            return render_template('CreateCampaign.html', error=success_msg), 409
    return render_template('CreateCampaign.html')


@app.route("/settings", methods=['GET', 'POST'])
@login_required
def global_settings_page():
    if request.method == "POST":
        # -- Add user returns a dict with action/result/reason keys.
        result = UsrMgmt.add_new_user(request.form, current_user.user_email)
        return jsonify(result)
    logs = AppManager.get_application_logs(current_user.user_email)
    return render_template("settings/GlobalSettings.html", logs=logs)


@app.route("/help", methods=["GET"])
@login_required
def HelpPage():
    return render_template("HelpPage.html")


@app.route("/listener", methods=['GET', 'POST'])
@login_required
def GlobalListenerPage():
    if app.config['listener_management'].check_tls_certificates() is False:
        flash('TLS certificates do not exist within the <install dir>/FudgeC2/Storage directory.')
    return render_template("listeners/listeners.html", test_data=app.config['listener_management'].get_active_listeners())


@app.route("/api/v1/listener/")
@login_required
def get_listener_details():

    return jsonify(app.config['listener_management'].get_active_listeners())


@app.route("/api/v1/listener/change", methods=['POST'])
@login_required
def Listener_Updates():
    form_response = app.config['listener_management'].update_listener_state(current_user.user_email, request.form)
    flash(form_response[1])
    return redirect(url_for('GlobalListenerPage'))


@app.route("/api/v1/listener/create", methods=['POST'])
@login_required
def create_new_listener():
    form_response = app.config['listener_management'].create_new_listener(current_user.user_email, request.form)
    if form_response[0] is False:
        return url_for('GlobalListenerPage'), 409
    else:
        return url_for('GlobalListenerPage'), 201

# -- CAMPAIGN SPECIFIC PAGES -- #
# ----------------------------- #



@app.route("/<cid>/settings", methods=['GET', 'POST'])
@login_required
def BaseImplantSettings(cid):
    # Allows updating the permissions of users in a campaign, and the visualisation of allowed users.
    g.setdefault('cid', cid)
    if request.method == "POST":
        UsrMgmt.AddUserToCampaign(current_user.user_email, request.form, cid)
        return redirect(url_for('BaseImplantSettings', cid=cid))
    else:
        users = UsrMgmt.get_current_campaign_users_settings_list(current_user.user_email, cid)
        return render_template("settings/CampaignSettings.html", users=users)


@app.route("/<cid>/implant/create", methods=['GET', 'POST'])
@login_required
def NewImplant(cid):
    # -- set SID and user DB to convert --#
    g.setdefault('cid', cid)
    if request.method == "POST":
        result, result_text = ImpMgmt.CreateNewImplant(cid, request.form, current_user.user_email)
        if result is True:
            return render_template('CreateImplant.html', success=result_text)
        else:
            return render_template('CreateImplant.html', error=result_text), 409
    return render_template('CreateImplant.html')


@app.route("/<cid>/implant/stagers", methods=["GET", "POST"])
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


@app.route("/<cid>/implant/active/<uik>", methods=["GET", "POST"])
@app.route("/<cid>/implant/active", methods=["GET", "POST"])
@login_required
def display_active_implant(cid, uik=None):
    g.setdefault('cid', cid)
    implants = ImpMgmt.get_active_campaign_implants(current_user.user_email, cid)
    if uik is not None:
        if type(implants) == list:
            for x in implants:
                if int(x['unique_implant_id']) == int(uik):
                    return render_template("implant/ActiveImplants.html", imp=implants, render=x)
    return render_template("implant/ActiveImplants.html", imp=implants)




@app.route("/<cid>/graphs", methods=['GET', 'POST'])
@login_required
def CampaignGraph(cid):
    g.setdefault('cid', cid)
    # -- If we receive a POST request then we will populate the page, this will be called AFTER the page has loaded.
    if request.method == "POST":
        blah = {'a': "1", 'b': "v"}
        return jsonify(blah)
    return render_template("CampaignGraph.html")


@app.route("/<cid>/logs", methods=["GET", "POST"])
@login_required
def CampaignLogs(cid):
    g.setdefault('cid', cid)
    if request.method == "POST":
        # -- Replace with pre-organised campaign logs - simplifies JS component.
        # Get_CampaignLogs
        return jsonify(ImpMgmt.Get_CampaignLogs(current_user.user_email, cid))
    return render_template("CampaignLogs.html")


@app.route("/<cid>/export_campaign", methods=["GET"])
@login_required
def export_campaign_by_cid(cid):
    g.setdefault('cid', cid)

    download = request.args.get('download', default=False, type=str)
    print("FILENAME IS: ", download)
    if download is not False:
        # STart download process.
        filename = ExpoManager.get_encrypted_file(current_user.user_email, cid, download)

        if filename is False:
            return "False"
        else:
            return send_file("../Storage/ExportedCampaigns/"+filename, as_attachment=True, attachment_filename="filename")
    else:
        export_result = ExpoManager.export_campaign_database(current_user.user_email, cid)
        if export_result is not False:
            print(export_result)
            return jsonify({"filename": export_result[0], "password": export_result[1]})

    return url_for("BaseImplantPage", cid=cid)


# -- Implant command execution -- #
@app.route("/<cid>/implant/register_cmd", methods=["POST"])
@login_required
def ImplantCommandRegistration(cid):
    if request.method == "POST":
        # -- This is the new format using ImpMgmt to handle validation of user and command.
        registration_response = ImpMgmt.ImplantCommandRegistration(cid, current_user.user_email, request.form)
        # -- Currently no return value is required. This should be defined.
        return jsonify(registration_response)
    return "000"


# -- Base for new endpoints.
@app.route("/campaign/<cid>/implant/get_all", methods=['POST'])
@app.route("/<cid>/", methods=['GET'])
@login_required
def get_all_active_implants(cid):
    g.setdefault('cid', cid)
    implant_list = UsrMgmt.campaign_get_all_implant_base_from_cid(current_user.user_email, cid)
    if implant_list is not False:
        if len(implant_list) > 0:
            return render_template("implant_input.html", Implants=implant_list)

    msg = "No implants have called back in association with this campaign - create an implant base and use the stager page."
    return render_template("ImplantMain.html", cid=cid, Msg=msg)


# Early API redevelopment:
@app.route("/api/v1/campaign")
@login_required
def get_user_campaigns():
    current_user.user_email = "admin"
    return jsonify(AppManager.get_all_user_campaigns(current_user.user_email))


@app.route("/api/v1/campaign/<cid>/implants/active")
@login_required
def get_active_implants(cid):
    current_user.user_email = "admin"
    a = ImpMgmt.get_active_campaign_implants(current_user.user_email, cid)
    return jsonify(a)


@app.route("/api/v1/campaign/<cid>/implants/queued", methods=['GET'])
@login_required
def get_implant_queued_commands(cid):
    # -- Get JSON blob which contains all implant commands and then registration state
    commands = ImpMgmt.Get_RegisteredImplantCommands(current_user.user_email, cid)
    return jsonify(commands)


@app.route("/api/v1/campaign/<cid>/implants/response/<implant_id>", methods=['GET'])
@app.route("/api/v1/campaign/<cid>/implants/response", methods=['GET'])
@login_required
def get_all_implant_responses(cid):
    # -- Javascript appears to not be printing out all entries
    if UsrMgmt.campaign_get_user_access_right_cid(current_user.user_email, cid):
        return jsonify(Imp.Get_CommandResult(cid))
    else:
        return str(0)


@app.route("/api/v1/campaign/<cid>/implants/state")
@login_required
def get_active_implants_state(cid):
    active_implant_list = UsrMgmt.campaign_get_all_implant_base_from_cid(current_user.user_email, cid)
    data = {}
    count = 1
    for implant in active_implant_list:
        implant_status_obj = {"status": None,
                              "title": implant['generated_title'],
                              "implant_id": implant['unique_implant_id'],
                              "last_checked_in": implant['last_check_in']
                              }
        beacon = implant['beacon']
        time_from_last_check_in = time.time() - implant['last_check_in']

        if time_from_last_check_in < beacon * 2.2:
            # A beacon of 60 seconds has request response == 120 seconds + jitter
            # meaning 132 seconds meaning a maximum of *2.2 delayed
            implant_status_obj['status'] = "Healthy"
        elif time_from_last_check_in < beacon * 3.5:
            implant_status_obj['status'] = "Delayed"
        else:
            implant_status_obj['status'] = "Unresponsive"

        data[count] = implant_status_obj
        count = count + 1
    return jsonify(data)
