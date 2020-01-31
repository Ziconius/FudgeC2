from Data.Database import Database
from Implant.Implant import ImplantSingleton
from Implant.ImplantFunctionality import ImplantFunctionality
from NetworkProfiles.NetworkProfileManager import NetworkProfileManager

import datetime

class ImplantManagement:
    # -- The implant management class is responsible for performing pre-checks and validation before sending data
    # --    to the Implant class
    db = Database()
    Imp = ImplantSingleton.instance
    ImpFunc = ImplantFunctionality()
    NetProMan = NetworkProfileManager()

    def _form_validated_obfucation_level_(self, form):
        if "obfuscation" in form:
            try:
                obfuscation_value = int(form['obfuscation'])

                if obfuscation_value < 0:
                    return 0
                elif obfuscation_value > 3:
                    return 3
                else:
                    return obfuscation_value
            except:
                return None
        return None

    def _validate_command(self, command):

        command_listing = self.ImpFunc.command_listing()

        # Process command output into:
        # :: load_module powerup
        if command.lstrip()[0:2] == "::":
            preprocessed_command = command.lstrip()[2:].lower().strip()
            for x in command_listing:
                if x['input'] in preprocessed_command:
                    a = preprocessed_command.partition(x['input'])
                    r_command = {"type": x['type'], "args": a[2].strip()}
                    return r_command, True
            return command, {"cmd_reg": {"result": False, "reason": "Unknown inbuilt command, i.e. '::'"}}
        elif command.lstrip()[0:1] == ":":
            preprocessed_command = command.lstrip()[1:].lower().strip()
            for x in command_listing:
                if x['input'] in preprocessed_command:
                    return command, {"cmd_reg": {"result": False, "reason": f"Potential typo found in \
command.A single colon was found, did you mean: :{command}. If not please submit a GitHub ticket with the \
submitted command."}}

        else:
            r_command = {"type": "CM", "args": command}
            return r_command, True

    def _validate_template_kill_date(self, form):
        if 'kill_date' in form:
            try:
                # Checking to ensure a the time is not before current time. # This time must match the webapp
                # submission format.
                user_time = datetime.datetime.strptime(form['kill_date'], '%d/%m/%Y, %H:%M')
                current_time = datetime.datetime.now()
                if user_time < current_time:
                    return None
                else:
                    return user_time
            except Exception as E:
                # print(f"Error: Implant format: {E}")
                return None

    def get_network_profile_options(self):
        return self.NetProMan.get_implant_template_code()

    def ImplantCommandRegistration(self, cid, username, form):
        # -- This should be refactored at a later date to support read/write changes to
        # --    granular controls on templates, and later specific implants
        User = self.db.campaign.Verify_UserCanWriteCampaign(username, cid)
        if User is False:
            return {"cmd_reg": {"result": False, "reason": "You are not authorised to register commands in this campaign."}}

        # -- Get All implants or implants by name then send to 'implant.py'
        # -- email, unique implant key, cmd
        if "cmd" in form and "ImplantSelect" in form:
            # -- before checking the database assess the cmd that was input.
            if len(form['cmd']) == 0:
                return {"cmd_reg": {"result": False, "reason": "No command submitted."}}

            processed_command, validated_command = self._validate_command(form['cmd'])
            if validated_command is not True:
                return validated_command

            # -- If validated_command is True then continue as it IS a valid command. N.b it may not be a legitimate command, but it is considered valid here.
            if form['ImplantSelect'] == "ALL":
                list_of_implants = self.db.implant.Get_AllGeneratedImplantsFromCID(cid)
            else:
                list_of_implants = self.db.implant.Get_AllImplantIDFromTitle(form['ImplantSelect'])

            # -- Access if this can fail. If empty return error.
            if len(list_of_implants) == 0:
                return {"cmd_reg": {"result": False, "reason": "No implants listed."}}

            for implant in list_of_implants:
                # -- Create return from the Implant.AddCommand() method.
                self.Imp.AddCommand(username, cid, implant['unique_implant_id'], processed_command)
            return {"cmd_reg": {"result": True, "reason": "Command registered"}}
        return {"cmd_reg": {"result": False, "reason": "Incorrect implant given, or non-existent active implant."}}


    def _verify_network_profile_(self, form):
        #print(f"ImpMan: {form}")
        network_protocols = {}
        for key in form:
            # print(f"{key}::{form[key]}::")
            a = self.NetProMan.validate_web_form(key, form[key])
            #print(":::",a)
            if a is not None:
                if a != False:
                    #print(f"Updating: {a}")
                    network_protocols.update(a)

        print(f"THIS IS THE RESULT OF THE NEW STUFF: {network_protocols}")
        return network_protocols


    def CreateNewImplant(self, cid, form, user):
        # TODO: Create checks for conflicting ports.
        implant_configuration = {
            "title": None,
            "description": None,
            "url": None,
            "beacon": None,
            "inital_delay": None,
            "obfuscation_level": None,
            "protocol": {},
            "kill_date": None
        }
        try:
            User = self.db.user.Get_UserObject(user)
            if User.admin == 0:
                return False, "Insufficient privileges."
            campaign_priv = self.db.campaign.Verify_UserCanWriteCampaign(user, cid)
            if campaign_priv is False:
                raise ValueError('User cannot write to this campaign.')

            if "CreateImplant" in form:
                obfuscation_level = self._form_validated_obfucation_level_(form)
                implant_configuration['kill_date'] = self._validate_template_kill_date(form)

                if obfuscation_level is None:
                    raise ValueError('Missing, or invalid obfuscation level.')
                else:
                    implant_configuration['obfuscation_level'] = obfuscation_level

                # -- Test for initial callback delay
                if 'initial_delay' in form:
                    if int(form['initial_delay']) and int(form['initial_delay']) >= 0:
                        implant_configuration['initial_delay'] = form['initial_delay']
                    else:
                        raise ValueError("Initial delay must be positive integer.")
                else:
                    raise ValueError("Initial delay not submitted.")
                # -- Test for beacon delay
                if 'beacon_delay' in form:
                    if int(form['beacon_delay']) >= 1:
                        implant_configuration['beacon'] = form['beacon_delay']
                    else:
                        raise ValueError("Beacon delay must an integer greater than 1 second.")
                else:
                    raise ValueError("No beacon delay submitted.")

                if form['title'] == "" or form['url'] == "" or form['description'] == "":
                    raise ValueError('Mandatory values left blank')
                else:
                    implant_configuration['title'] = form['title']
                    implant_configuration['url'] = form['url']
                    implant_configuration['description'] = form['description']
                    implant_configuration['beacon'] = form['beacon_delay']

                # Verify the input against all loaded network profiles.
                validated_network_protocols = self._verify_network_profile_(form)
                if len(validated_network_protocols) != 0:
                    implant_configuration['protocol'].update(validated_network_protocols)
                else:
                    raise ValueError("Error: No valid network profiles submitted.")


                implant_creation = self.db.implant.create_new_implant_template(user, cid, implant_configuration)
                if implant_creation is True:
                    return True, "Implant created."
                else:
                    raise ValueError(f"Error: {implant_creation}")

        except Exception as E:
            return False, E

    def Get_RegisteredImplantCommands(self, username, cid=0):
        # -- Return list of dictionaries, not SQLAlchemy Objects.
        if self.db.campaign.Verify_UserCanAccessCampaign(username, cid):
            commands = self.db.implant.Get_RegisteredImplantCommandsFromCID(cid)
            to_dict = []
            for x in commands:
                a = x.__dict__
                if '_sa_instance_state' in a:
                    del a['_sa_instance_state']
                to_dict.append(a)
            return to_dict
        else:
            return False

    def Get_CampaignLogs(self, username, cid):
        User = self.db.campaign.Verify_UserCanReadCampaign(username, cid)
        if User is False:
            return {
                "cmd_reg": {"result": False, "reason": "You are not authorised to view commands in this campaign."}}
        return self.db.Log_GetCampaignActions(cid)

    def get_active_campaign_implants(self, user, campaign_id):
        if self.db.campaign.Verify_UserCanAccessCampaign(user, campaign_id):
            raw = self.db.implant.Get_AllGeneratedImplantsFromCID(campaign_id)
            # Removing the SQLAlchemy object.
            tr = []
            for num, item in enumerate(raw):
                del item['_sa_instance_state']
                tr.append(item)
            return tr
        else:
            return False
