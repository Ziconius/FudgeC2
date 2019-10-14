from Data.Database import Database
from Implant.Implant import ImplantSingleton


class ImplantManagement:
    # -- The implant management class is responsible for performing pre-checks and validation before sending data
    # --    to the Implant class
    db = Database()
    Imp = ImplantSingleton.instance

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
                print("None integer submitted.")
                return None
        return None

    def _validate_command(self, command):
        command_listing = [
            {
                "type": "FU",
                "args": "base64-file::filelocation",
                "input": "upload_file"
            },
            {
                "type": "FD",
                "args": "base64 target file",
                "input": "download_file"
            },
            {
                "type": "PS",
                "args": "sound file location (on Fudge)",
                "input":"play_audio"
            },
            {
                "type": "EP",
                "args": None,
                "input":"enable_persistence"
            },
            {
                "type": "SI",
                "args": None,
                "input":"sys_info"
            },
            {
                "type": "EC",
                "args": None,
                "input": "export_clipboard"
            },
            {
                "type":"LM",
                "args":None,
                "input": "load_module"
            }
        ] # FU,FD,PS,EP,SI, EC

        # Process command output into:
        if command.lstrip()[0:2] == "::":
            preprocessed_command = command.lstrip()[2:].lower().strip()
            for x in command_listing:
                if x['input'] in preprocessed_command:
                    a = preprocessed_command.partition(x['input'])
                    r_command = { "type":x['type'], "args":a[2].strip()}
                    return r_command, True
            return command, {"cmd_reg": {"result": False, "reason": "Unknown inbuilt command, i.e. '::'"}}
        else:
            r_command = {"type": "CM", "args": command}

        return r_command, True

    def ImplantCommandRegistration(self, cid, username, form):
        # -- This should be refactored at a later date to support read/write changes to
        # --    granular controls on templates, and later specific implants
        # print("CID: ",cid,"\nUSR: ",username,"\nCMD: ",form)
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

    def CreateNewImplant(self,cid, form, user):
        # TODO: Create checks for conflicting ports.
        implant_configuration = {
            "title": None,
            "description": None,
            "url": None,
            "beacon": None,
            "inital_delay": None,
            "obfuscation_level": None,
            "protocol": {
                "comms_http": None,
                "comms_https": None,
                "comms_binary": None,
                "comms_dns": None
            }
        }
        print(form)
        User = self.db.user.Get_UserObject(user)
        if User.admin == 0:
            return False, "Insufficient privileges."
        CampPriv = self.db.campaign.Verify_UserCanWriteCampaign(user, cid)
        if CampPriv is False:
            return False, "User cannot write to this campaign."

        try:
            if "CreateImplant" in form:
                obfuscation_level = self._form_validated_obfucation_level_(form)
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

                a = {"comms_http": "http-port",
                     "comms_https": "https-port",
                     "comms_dns": "dns-port",
                     "comms_binary": "binary-port"}
                for element in a.keys():
                    print("::", element)
                    if element in form:
                        # print("@@", form[a[element]])
                        if int(form[a[element]]):
                            if int(form[a[element]]) > 0 or int(form[a[element]]) < 65536:
                                # print(int(form[a[element]]))
                                implant_configuration["protocol"][element] = int(form[a[element]])
                            else:
                                raise ValueError("Submitted port for {} is out of range".format(a[element]))
                        else:
                            # print(form[element])
                            raise ValueError("Ports must be submitted as an integer")

                protocol_set = False
                for proto in implant_configuration['protocol'].keys():
                    if implant_configuration['protocol'][proto] is None:
                        protocol_set = True
                if protocol_set is False:
                    raise ValueError('No protocol selected, ensure a protocol and port are selected.')

                # print("Final configuration:")
                # for element in implant_configuration.keys():
                #     print(element,": ",implant_configuration[element])

                a = self.db.implant.create_new_implant_template(user, cid, implant_configuration)
                if a is True:
                    return True, "Implant created."
                else:
                    raise ValueError("Error creating entry. Ensure implant title is unique.")

        except Exception as E:
            return False, E

        return

    def Get_RegisteredImplantCommands(self, username, cid=0):
        # -- Return list of dictionaries, not SQLAlchemy Objects.
        if self.db.campaign.Verify_UserCanAccessCampaign(username, cid):
            Commands = self.db.implant.Get_RegisteredImplantCommandsFromCID(cid)
            toDict = []
            for x in Commands:
                a = x.__dict__
                if '_sa_instance_state' in a:
                    del a['_sa_instance_state']
                toDict.append(a)
            return toDict
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
            return self.db.implant.Get_AllGeneratedImplantsFromCID(campaign_id)
        else:
            return False
