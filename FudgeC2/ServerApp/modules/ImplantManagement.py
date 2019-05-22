from Data.Database import Database
from Implant.Implant import ImplantSingleton
import time
class ImplantManagement():
    # -- The implant management class is responsible for performing pre-checks and validation before sending data
    # --    to the Implant class
    db = Database()
    Imp = ImplantSingleton.instance

    def _form_validated_obfucation_level_(self, form):
        for x in form:
            if "obfus" in x:
                a  = x.split("-")
                print("ll", a[1])
                # -- returning first value, we should only receive a single entry.
                try:
                    return int(a[1])
                except:
                    return None
        return None


    def _validate_command(self, command):
        # -- TODO: Check if type needs to be enforced.
        special_cmd = ["sys_info"]
        if command[0:2] == "::":
            preprocessed_command = command[2:].lower().strip()
            if preprocessed_command in special_cmd:
                postprocessed_command = ":: "+preprocessed_command
                return postprocessed_command, True
            return command, {"cmd_reg":{"result":False, "reason":"Unknown inbuilt command, i.e. '::'"}}
        return command, True


    def ImplantCommandRegistration(self, cid , username, form):
        # -- This should be refactored at a later date to support read/write changes to
        # --    granular controls on templates, and later specific implants
        #print("CID: ",cid,"\nUSR: ",username,"\nCMD: ",form)
        User = self.db.Verify_UserCanWriteCampaign(username,cid)
        if User == False:
            return {"cmd_reg":{"result":False,"reason":"You are not authorised to register commands in this campaign."}}

        # -- Get All implants or implants by name then send to 'implant.py'
        # -- email, unique implant key, cmd
        if "cmd" in form and "ImplantSelect" in form:
            # -- before checking the database assess the cmd that was input.
            processed_command, validated_command = self._validate_command(form['cmd'])
            if validated_command != True:
                return validated_command

            # -- If validated_command is True then continue as it IS a valid command. N.b it may not be a legitimate command, but it is considered valid here.
            if form['ImplantSelect'] == "ALL":
                ListOfImplants = self.db.Get_AllGeneratedImplantsFromCID(cid)
            else:
                ListOfImplants= self.db.Get_AllImplantIDFromTitle(form['ImplantSelect'])
            # -- Access if this can fail. If empty return error.
            if len(ListOfImplants) == 0:
                return {"cmd_reg":{"result":False,"reason":"No implants listed."}}
            for implant in ListOfImplants:
                # -- Create return from the Implant.AddCommand() method.
                self.Imp.AddCommand(username,cid,implant['unique_implant_id'], processed_command)
            return {"cmd_reg":{"result":True,"reason":"Command registered"}}
        return {"cmd_reg":{"result":False,"reason":"Incorrect implant given, or non-existant active implant."}}

    def CreateNewImplant(self,cid,form, user):
        # -- This is creating a new Implant Template
        User = self.db.Get_UserObject(user)
        if User.admin == 0:
            return False, "Insufficient Priviledges"
        CampPriv = self.db.Verify_UserCanWriteCampaign(user,cid)
        if CampPriv == False:
            return False, "User cannot write to this campaign"
        # -- From here we know the user is able to write to the Campaign and an admin.

        try:
            if "CreateImplant" in form:
                obfuscation_level = self._form_validated_obfucation_level_(form)
                if obfuscation_level == None:
                    print("OL", obfuscation_level)
                    raise ValueError('Missing, or invalid obfuscation levels')
                if form['title'] == "" or form['url'] == "" or form['description'] == "":
                    raise ValueError('Mandatory values left blank')
                title = form['title']
                url=form['url']
                port = form['port']
                description= form['description']
                beacon=form['beacon_delay']
                initial_delay=form['initial_delay']
                comms_http = 0
                comms_https = 0
                comms_dns = 0
                comms_binary = 0
                try:
                    port = int(port)
                except:
                    if type(port) != int:
                        raise ValueError('Port is required as integer')
                # -- Comms check --#
                if "comms_http" in form:
                    comms_http = 1
                if "comms_https" in form:
                    comms_https = 1
                if "comms_dns" in form :
                    comms_dns = 1
                if "comms_binary" in form :
                    comms_binary = 1
                if comms_binary == 0 and comms_dns == 0 and comms_http == 0 and comms_https == 0:
                    raise ValueError('No communitcation channel selected. ')
                if comms_http ==1 and comms_https == 1:
                    raise ValueError("Please select HTTP or HTTPS")
                a = self.db.Add_Implant(cid, title ,url,port,beacon,initial_delay,comms_http,comms_https,comms_dns,comms_binary,description,obfuscation_level)
                if a == True:
                    return True, "Implant created."
                else:
                    raise ValueError("Error creating entry. Ensure filename is unique")
        except Exception as e:
            print("NewImplant: ",e)
            # --  returning page with generic Error --#
            return False, e

    def Get_RegisteredImplantCommands(self, username, cid=0):
        # -- Return list of dictionaries, not SQLAlchemy Objects.
        if self.db.Verify_UserCanAccessCampaign(username, cid):
            Commands = self.db.Get_RegisteredImplantCommandsFromCID(cid)
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
        User = self.db.Verify_UserCanReadCampaign(username, cid)
        if User == False:
            return {
                "cmd_reg": {"result": False, "reason": "You are not authorised to view commands in this campaign."}}
        return self.db.Log_GetCampaignActions(cid)
