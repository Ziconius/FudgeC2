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
            return "Insufficient Priviledges"
        CampPriv = self.db.Verify_UserCanWriteCampaign(user,cid)
        if CampPriv == False:
            return "User cannot write to this campaign"
        # -- From here we know the user is able to write to the Campaign and an admin.

        try:
            if "CreateImplant" in form:
                obfuscation_level = self._form_validated_obfucation_level_(form)
                if obfuscation_level == None:
                    print("OL", obfuscation_level)
                    raise ValueError('Missing, or invalid obfuscation levels')
                if form['title'] =="" or form['url'] =="" or form['description'] == "":
                    raise ValueError('Mandatory values left blank')
                title = form['title']
                url=form['url']
                port = form['port']
                description= form['description']
                beacon=form['beacon_delay']
                initial_delay=form['initial_delay']
                comms_http = 0
                comms_dns = 0
                comms_binary = 0
                try:
                    port = int(port)
                except:
                    if type(port) != int:
                        raise ValueError('Port is required as integer')
                # -- Comms check --#
                if "comms_http" in form :
                    comms_http = 1
                if "comms_dns" in form :
                    comms_dns = 1
                if "comms_binary" in form :
                    comms_binary = 1
                if comms_binary == 0 and comms_dns == 0 and comms_http ==0:
                    raise ValueError('No communitcation channel selected. ')
                a = self.db.Add_Implant(cid, title ,url,port,beacon,initial_delay,comms_http,comms_dns,comms_binary,description,obfuscation_level)
                if a == True:
                    return "Implant created."
                else:
                    raise ValueError("Error creating entry. Ensure filename is unique")
        except Exception as e:
            print("NewImplant: ",e)
            # -- Implicting returning page with Error --#
            return e

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

    def ReorderList(self, List, Item, event=None, key='time'):
        # print(":: ",Item)
        if len(List) == 0:
            Item['lo-time'] = Item[key]
            if key == 'time':
                Item['time-type'] = 'time'
            else:
                Item['time-type'] = 'read_by_implant'
            Item['event'] = event
            List.append(Item)
            # print(List)
            return List
        # print(Item)
        for index, value in enumerate(List):
            # print("@@",index, value)
            # print(value['lo-time'], Item[key])
            # print(value['lo-time'] - Item[key])
            if value['lo-time'] < Item[key]:
                # print(key, Item)
                Item['event'] = event
                Item['lo-time'] = Item[key]
                if key == 'time':
                    Item['time-type'] = 'time'
                else:
                    Item['time-type'] = 'read_by_implant'
                print(key, "::", Item['time-type'], Item['lo-time'], Item)
                List.insert(index - 1, Item)
                break
        return List


    def Get_CampaignLogs(self, username, cid):
        User = self.db.Verify_UserCanReadCampaign(username, cid)
        if User == False:
            return {
                "cmd_reg": {"result": False, "reason": "You are not authorised to view commands in this campaign."}}
        return self.db.Log_GetCampaignActions(cid)


    def Get_ChronologicallyOrderedCampaignLogsJSON(self,username,cid):
        # -- TODO: BUG. This doesn't properly return the list, all cmd_reg elements replaced by
        # --     cmd_pickup. Likely an issue with the way the list is being structured.
        unorder_logs = self.Get_CampaignLogsJson(username,cid)

        final_list = []

        for key in unorder_logs.keys():
            if key == "metadata":
                break
            for i in unorder_logs[key]:
                #print(unorder_logs[key][i])
                if key == "commands":
                    #print(unorder_logs[key][i]['time'])
                    a = unorder_logs[key][i]
                    final_list = self.ReorderList(final_list, a, "cmd_reg")
                    for x in final_list:
                        print("''''",x['event'])
                    a = None
                    a = unorder_logs[key][i]
                    print("%%",a)
                    if unorder_logs[key][i]['read_by_implant'] != 0:
                        print("Implant read")
                        final_list = self.ReorderList(final_list, a,"imp_read", 'read_by_implant')
                    for x in final_list:
                        print("''''",x['event'])
                    # do pick up
                elif key == "implants":
                    final_list = self.ReorderList(final_list, unorder_logs[key][i], "new_imp")
                    pass
                elif  key == "response":
                    final_list = self.ReorderList(final_list, unorder_logs[key][i], "response")

        ordered_logs = {}
        return final_list

    def Get_CampaignLogsJson(self, username, cid):
        a = '''
        Get all data on a campaign
         - Registered commands
         - implants
          - response implant_logs
           - implant_response

        timeline pathways:
         - New active implant registrations (AllGeneratedImplants)
         - Command registrations (RegistererdImplantsCommands)
         - command pickup (RegistererdImplantsCommands)
         - Implant response (Campaign Implant Response
        '''

        User = self.db.Verify_UserCanReadCampaign(username, cid)
        if User == False:
            return {"cmd_reg": {"result": False, "reason": "You are not authorised to register commands in this campaign."}}

        EarliestInteraction = 0
        LastestInteraction = 0
        def TimeCompare(UnixTime, EarliestInteraction, LastestInteraction):

            if UnixTime < EarliestInteraction or EarliestInteraction == 0:
                EarliestInteraction = UnixTime
            if UnixTime > LastestInteraction:
                LastestInteraction = UnixTime
            return EarliestInteraction, LastestInteraction

        normalised_data = {"implants": {},
                           "commands": {},
                           "response": {},
                           "metadata": {},
                           }

        aa = self.db.Get_AllGeneratedImplantsFromCID(cid)
        bb = self.db.Get_RegisteredImplantCommandsFromCID(cid)
        cc = self.db.Get_CampaignImplantResponses(cid)

        counter = 0
        # -- Normalise generated implants
        for x in aa:
            b = x
            if '_sa_instance_state' in b:
                del b['_sa_instance_state']
            normalised_data["implants"][counter]= b
            counter +=1
        # -- Normalise RegisteredImplants
        counter = 0
        for gg in bb:
            jj = gg.__dict__
            if '_sa_instance_state' in jj:
                del jj['_sa_instance_state']
            normalised_data['commands'][counter]=jj
            counter +=1
        # -- Get command response
        counter = 0
        for x in cc:
            normalised_data['response'][counter]=x
            counter+=1

        for keys in normalised_data.keys():
            for x in normalised_data[keys]:
                if 'time' in normalised_data[keys][x]:
                    # print("::",keys)
                    EarliestInteraction, LastestInteraction = TimeCompare(normalised_data[keys][x]['time'],EarliestInteraction, LastestInteraction)
                if 'read_by_implant' in normalised_data[keys][x]:
                    EarliestInteraction, LastestInteraction = TimeCompare(normalised_data[keys][x]['read_by_implant'],EarliestInteraction, LastestInteraction)
                elif 'blah' in normalised_data[keys][x]:
                    print("No.")

        from datetime import datetime

        # print(datetime.fromtimestamp(EarliestInteraction))
        # print(datetime.fromtimestamp(LastestInteraction))
        normalised_data['metadata']['earliest_interaction'] = EarliestInteraction
        normalised_data['metadata']['last_interaction'] = LastestInteraction
        return normalised_data