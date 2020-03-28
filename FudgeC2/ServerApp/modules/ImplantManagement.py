from Data.Database import Database
from Implant.Implant import ImplantSingleton
from Implant.ImplantFunctionality import ImplantFunctionality
from NetworkProfiles.NetworkProfileManager import NetworkProfileManager

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ImplantManagement:
    # -- The implant management class is responsible for performing pre-checks and validation before sending data
    # --    to the Implant class
    db = Database()
    Imp = ImplantSingleton.instance
    ImpFunc = ImplantFunctionality()
    NetProMan = NetworkProfileManager()

    def _form_validated_obfucation_level_(self, form):
        # Checking if obfuscation if an integer between 0-4, if not return None to raise an error.
        try:
            obfuscation_value = int(form['obfuscation'])

            if obfuscation_value < 0:
                obfuscation_value = 0
            elif obfuscation_value > 4:
                obfuscation_value = 4
            return obfuscation_value
        except:
            logger.warning(f"{self}")
            return None

    def _validate_command(self, command):
        # Validate the command is one of 2 thing either a Powershell direct execution or a
        # builtin command using :: notation.
        # Once validate this processes the command into a "type" and "arg", both strings.

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
            return command, "Unknown inbuilt command (::). See help page for more info."
        elif command.lstrip()[0:1] == ":":
            preprocessed_command = command.lstrip()[1:].lower().strip()
            for x in command_listing:
                if x['input'] in preprocessed_command:
                    return command, (f"Potential typo found in command. A single colon was found, did you mean :"
                                     f"{command}. If not please raise a GitHub ticket with the submitted command.")

        else:
            r_command = {"type": "CM", "args": command}
            return r_command, True

    def _validate_template_kill_date(self, form):
        if 'kill_date' in form:
            try:
                # Checking to ensure a the time is not before current time.
                #  This time must match the webapp submission format.
                print(form)
                user_time = datetime.strptime(form['kill_date'], '%d/%m/%Y, %H:%M')
                current_time = datetime.now()
                if user_time < current_time:
                    return None
                else:
                    # Reformatting the datetime to match implant datetime format string
                    return datetime.strftime(user_time, '%Y-%m-%d %H:%M:%S')
            except Exception as E:
                print(E)
                error_logging.error(f"kill_date vaule not in form: {__name__}", E)
                return None

    def _validate_template_operating_hours(self, form):
        # This returns a dict no matter what.
        time_dict = {}
        timemask = "%H:%M"
        if "oh_start" in form and "oh_stop" in form:
            time_dict['oh_start'] = form['oh_start']
            time_dict['oh_stop'] = form['oh_stop']
            try:
                start = datetime.strptime(time_dict['oh_start'], timemask)
                stop = datetime.strptime(time_dict['oh_stop'], timemask)
                # Ensure the start is less than stop
                if start >= stop:
                    print(f"Start {start} is greater than stop {stop}")
                return time_dict
            except Exception as e:
                print(f"Formatting error: {e}")
                return {}
        else:
            return {}


    def get_network_profile_options(self):
        return self.NetProMan.get_implant_template_code()

    def implant_command_registration(self, cid, username, form):
        result_msg = "Unknown error."
        try:
            User = self.db.campaign.Verify_UserCanWriteCampaign(username, cid)
            if User is False:
                result_msg = "You are not authorised to register commands in this campaign."
                raise ValueError

            if "cmd" not in form and "ImplantSelect" not in form:
                result_msg = f"Malformed request: {form}"
                raise ValueError

            if len(form['cmd']) == 0:
                result_msg = "No command submitted."
                raise ValueError

            processed_command, validated_command = self._validate_command(form['cmd'])
            if validated_command is not True:
                result_msg = validated_command
                raise ValueError

            result = self.ImpFunc.validate_pre_registered_command(processed_command)
            if result is not True:
                result_msg = result
                raise ValueError

            if form['ImplantSelect'] == "ALL":
                list_of_implants = self.db.implant.Get_AllGeneratedImplantsFromCID(cid)
            else:
                list_of_implants = self.db.implant.Get_AllImplantIDFromTitle(form['ImplantSelect'])

            # Check if any implants have been returned against the user submitted values.
            if len(list_of_implants) == 0:
                result_msg = "No implants listed."
                raise ValueError

            # Assuming all checks have passed no Exceptions will have been raised and we can register commands.
            for implant in list_of_implants:
                self.Imp.add_implant_command_to_server(username, cid, implant['unique_implant_id'], processed_command)
            return {"result": True, "reason": "Command registered"}
        except:
            return {"result": False, "reason": result_msg}

    def _verify_network_profile_(self, form):
        network_protocols = {}
        for key in form:
            a = self.NetProMan.validate_web_form(key, form[key])
            if a is not None:
                if a != False:
                    network_protocols.update(a)
        return network_protocols


    def create_new_implant(self, cid, form, user):
        # TODO: Create checks for conflicting ports.
        implant_configuration = {
            "title": None,
            "description": None,
            "url": None,
            "beacon": None,
            "inital_delay": None,
            "obfuscation_level": None,
            "encryption": [],
            "protocol": {},
            "kill_date": None,
            "operating_hours": None
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
                implant_configuration['operating_hours'] = self._validate_template_operating_hours(form)

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

                if "staticEncryption" in form:
                    implant_configuration['encryption'].append('static_encryption')
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
            print(E)
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
