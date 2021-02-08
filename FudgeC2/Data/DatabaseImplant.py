import time
import random
import secrets
import string

from Data.models import ImplantResponse, ImplantTemplate, ImplantCommands, Campaigns, CampaignUsers, GeneratedImplants, HostData
from Data.CampaignLogging import CampaignLoggingDecorator

CL = CampaignLoggingDecorator()


class DatabaseImplant:

    def __init__(self, source_database, session):
        # TODO: Check session type
        self.Session = session
        self.db_methods = source_database

    def Get_AllImplantIDFromTitle(self, implant_title):
        # -- Return list containing generated implant dictionaries.
        implant_object = self.Session.query(GeneratedImplants,
                                            ImplantTemplate).filter(ImplantTemplate.iid == GeneratedImplants.iid,
                                                             GeneratedImplants.generated_title == implant_title).all()

        implant_object = self.db_methods.__splice_implants_and_generated_implants__(implant_object)
        return implant_object

    # TODO: Add logging
    @CL.new_implant_template_created
    def create_new_implant_template(self, user, cid, config):
        stager_key = random.randint(10000, 99999)
        new_implant = ImplantTemplate(
            cid=cid,
            title=config['title'],
            description=config['description'],
            stager_key=stager_key,
            callback_url=config['url'],
            beacon=config['beacon'],
            encryption=config['encryption'],
            kill_date=config['kill_date'],
            initial_delay=config['initial_delay'],
            obfuscation_level=config['obfuscation_level'],
            network_profiles=config['protocol'],
            operating_hours=config['operating_hours']
        )
        self.Session.add(new_implant)
        try:
            self.Session.commit()
            return True

        except Exception as e:
            error = f"Error in create_new_implant_template() SQLAlc error: {e}"
            return error

    def Get_AllImplantBaseFromCid(self, cid):
        # -- THIS NEED TO BE REBUILT
        all_implants = self.Session.query(ImplantTemplate).filter(ImplantTemplate.cid == cid).all()
        processed_implants = []
        for implant in all_implants:
            b = implant.__dict__
            if '_sa_instance_state' in b:
                del b['_sa_instance_state']
            processed_implants.append(b)

        if processed_implants is not None:
            return processed_implants
        else:
            return []

    def Get_AllGeneratedImplantsFromCID(self, campaign_id):
        raw_implants = self.Session.query(GeneratedImplants,
                                          ImplantTemplate).filter(GeneratedImplants.iid == ImplantTemplate.iid,
                                                                  ImplantTemplate.cid == campaign_id).all()

        generated_implants = self.db_methods.__splice_implants_and_generated_implants__(raw_implants)
        if generated_implants is not None:
            return generated_implants
        else:
            return False

    def Get_GeneratedImplantDataFromUIK(self, UIK):
        # -- Pulls all configuration data for a generated implant based on UIK.
        # --    Used when implants checks in.
        result = self.Session.query(GeneratedImplants, ImplantTemplate).filter(ImplantTemplate.iid == GeneratedImplants.iid,
                                                                        GeneratedImplants.unique_implant_id == UIK
                                                                        ).first()
        if result is not None:
            implant_list = self.db_methods.__splice_implants_and_generated_implants__(result)
            for implant_template in implant_list:
                if '_sa_instance_state' in implant_template:
                    del implant_template['_sa_instance_state']

            if implant_list is not None:
                return implant_list[0]
            else:
                return False

    def get_all_implants_by_user(self, user_email):
        # Gets all implants across all campaigns for a specific user.
        user_id = self.db_methods.__get_userid__(user_email)
        if user_id is False:
            return []

        campaigns = self.Session.query(CampaignUsers.cid).filter(CampaignUsers.uid == user_id).all()
        all_active_implants = []
        for campaign in campaigns:
            all_active_implants.append(self.Get_AllGeneratedImplantsFromCID(campaign[0]))

        processes_active_implants = []
        for implant_by_cid in all_active_implants:
            for implant in implant_by_cid:
                entry = {
                    "implant_id": implant['unique_implant_id'],
                    "campaign_id": implant['cid']
                     }
                processes_active_implants.append(entry)
        return processes_active_implants

    @CL.log_implant_activation
    def Register_NewImplantFromStagerKey(self, stager_key):
        # -- We are registering a NEW implant and generating a unique_stager_key (or UIK)
        # -- Moving forward all reference to ImplantKey/UII should be changed to StagerID

        implant = self.Session.query(ImplantTemplate).filter(ImplantTemplate.stager_key == stager_key).first()
        if implant is not None:
            unique_implant_key = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
            # new_title = str(implant.title) + "_" + str(unique_implant_key)
            new_title = f"{implant.title}_{unique_implant_key}"
            generated_implant = GeneratedImplants(unique_implant_id=unique_implant_key,
                                                  last_check_in=0,
                                                  current_beacon=implant.beacon,
                                                  iid=implant.iid,
                                                  generated_title=new_title,
                                                  time=int(time.time()))
            self.Session.add(generated_implant)
            try:
                self.Session.commit()
                self.Session.query(GeneratedImplants).first()

            except Exception as e:
                print("db.Add_Implant: ", e)
                return False

            active_implant_record = self.Session.query(GeneratedImplants, ImplantTemplate).filter(
                ImplantTemplate.iid == GeneratedImplants.iid,
                GeneratedImplants.unique_implant_id == unique_implant_key).first()

            active_implant_record = self.db_methods.__splice_implants_and_generated_implants__(active_implant_record)

            # -- Return Raw objects, and caller to manage them,
            return active_implant_record
        return False

    def Set_GeneratedImplantCopy(self, new_spliced_implant_data, delivered_payload, cleartext_implant):
        # This will store a copy of the PS implant to the "Generated_Implants" table
        #   This will allow RT to send analysable copy to BT for signaturing etc.
        try:
            uik = new_spliced_implant_data['unique_implant_id']
            self.Session.query(GeneratedImplants).filter(
                GeneratedImplants.unique_implant_id == uik).update({"implant_copy": cleartext_implant, "delivered_payload": delivered_payload})

            self.Session.commit()
        except Exception as E:
            print(E)
            pass

    # TODO: Create logging
    @CL.update_implant_check_in
    def Update_ImplantLastCheckIn(self, cid, generated_implant_key, c2_protocol):
        # -- TODO: Create error handling around invalid GeneratedImplantKey
        self.Session.query(GeneratedImplants).filter(
            GeneratedImplants.unique_implant_id == generated_implant_key).update(
                {"last_check_in": (int(time.time())),
                 "last_check_in_protocol": c2_protocol
                 })
        self.Session.commit()
        return True

    @CL.log_cmdreg
    def Register_ImplantCommand(self, username, uik, command,  cid=0):
        # -- Requirements: username unique_implant_key, command
        # -- Checks: User can register commands against a generated implant

        uid = self.db_methods.__get_userid__(username)

        result = self.Session.query(CampaignUsers,
                                    ImplantTemplate,
                                    GeneratedImplants
                                    ).filter(
                            CampaignUsers.uid == uid,
                            Campaigns.cid == CampaignUsers.cid,
                            ImplantTemplate.cid == Campaigns.cid,
                            ImplantTemplate.iid == GeneratedImplants.iid,
                            GeneratedImplants.unique_implant_id == uik).all()

        if len(result) == 0:
            return False

        # Check existing command_id values to avoid collisions
        existing_implant_logs = self.Session.query(ImplantCommands)
        tmp_command_id = []
        for log in existing_implant_logs:
            tmp_command_id.append(log.__dict__['command_id'])
        while True:
            cmd_id = secrets.token_hex(12)
            if cmd_id not in tmp_command_id:
                break

        for line in result:
            if line[0].permissions == 2:
                cid = line[0].cid
                # Get all ImplantLog: check for command_id
                new_implant_log = ImplantCommands(cid=cid,
                                                  uid=uid,
                                                  time=time.time(),
                                                  log_entry=command,
                                                  uik=uik,
                                                  read_by_implant=0,
                                                  command_id=cmd_id)

                self.Session.add(new_implant_log)
                try:
                    self.Session.commit()
                    self.Session.query(ImplantCommands).first()
                    return True
                except Exception as e:
                    print("db.Register_ImplantCommand: ", e)
                    return False
            else:
                # -- Incase non 0/1 response --#
                return False

    def Get_RegisteredImplantCommandsFromUIK(self, unique_implant_key):
        # -- Return List
        logs = self.Session.query(ImplantCommands).filter(ImplantCommands.uik == unique_implant_key).all()
        if logs is not None:
            return logs
        else:
            return []

    def get_registered_implant_commands_by_command_id(self, command_id):
        result = self.Session.query(ImplantCommands).filter(ImplantCommands.command_id == command_id).all()
        return self.db_methods.__sa_to_dict__(result)

    def Get_RegisteredImplantCommandsFromCID(self, campaign_id):
        # Used by web app.
        logs = self.Session.query(ImplantCommands).filter(ImplantCommands.cid == campaign_id).all()
        if len(logs) > 0:
            return logs
        else:
            return []

    @CL.log_cmdpickup
    def Register_ImplantCommandPickup(self, record, protocol):
        # DEV NOTES: DwarvenBlacksmith: This will require the command to be cast from string to dict.
        self.Session.query(ImplantCommands).filter(
            ImplantCommands.uik == record.uik,
            ImplantCommands.log_entry == record.log_entry,
            ImplantCommands.time == record.time).update({'read_by_implant': int(time.time()), 'c2_protocol': str(protocol)})
        try:
            self.Session.commit()
            return True
        except Exception as E:
            print("Exception: ", E)
            return False

    @CL.log_cmdresponse
    def Register_ImplantResponse(self, command_id, response, c2_protocol):
        # -- TODO: REBUILD
        # Pull back the first record which matches the UIK, contain both the Campaign the IID
        #   is associated from the implant the UIk is associated with.
        info = self.Session.query(ImplantTemplate, Campaigns, GeneratedImplants).filter(
            Campaigns.cid == ImplantTemplate.cid).filter(
            ImplantTemplate.iid == GeneratedImplants.iid).filter(
            GeneratedImplants.unique_implant_id == ImplantCommands.uik,
            ImplantCommands.command_id == command_id).first()

        # iid = info[0].iid
        cid = info[1].cid
        uik = info[2].unique_implant_id
        response_logs = ImplantResponse(cid=cid, uik=uik, log_entry=response, time=int(time.time()), command_id=command_id)
        self.Session.add(response_logs)
        try:
            self.Session.commit()
            return True
        except Exception as E:
            print(E)

    def update_host_data(self, unique_implant_key, host_data):
        # This will update the table with the data from the ImplantResponseProcessor class.
        # Data will be a list of columns, and their data.

        # self.Session.query(ImplantCommands).filter(
        #     ImplantCommands.uik == record.uik,
        #     ImplantCommands.log_entry == record.log_entry,
        #     ImplantCommands.time == record.time).update(
        #     {'read_by_implant': int(time.time()), 'c2_protocol': str(protocol)})


        for item in host_data:
            for key in item.keys():
                print(f"Updating host data with: {key}:{item[key]}")
                try:
                    self.Session.query(HostData).filer(HostData.unique_implant_key == unique_implant_key).update(
                        {key:item[key]}
                    )
                except Exception as E:
                    print(E)


        return

    def Get_CampaignImplantResponses(self, cid):
        # Used by web app
        # To be removed
        # -- TODO: Refactor
        a = self.Session.query(ImplantResponse).filter(ImplantResponse.cid == cid).all()
        return_list = []
        for x in a:
            a = x.__dict__
            if '_sa_instance_state' in a:
                del a['_sa_instance_state']
            b = self.Session.query(GeneratedImplants.generated_title).filter(
                GeneratedImplants.unique_implant_id == a['uik']).first()

            if b is not None:
                a['title'] = b[0]
            return_list.append(a)
        return return_list

    def get_implant_responses(self, implant_id):
        responses = self.Session.query(ImplantResponse).filter(ImplantResponse.uik == implant_id).all()
        processed_responses = self.db_methods._sqlalc_rows_to_list(responses)
        return processed_responses

    def get_implant_information(self, implant_id):
        information = self.Session.query(GeneratedImplants, ImplantTemplate).filter(
            ImplantTemplate.iid == GeneratedImplants.iid,
            GeneratedImplants.unique_implant_id == implant_id).first()
        return self.db_methods._combine_sqlacl_dicts(information)

    def get_implant_templates_by_campaign_id(self, campaign_id):
        sql_acl_obj = self.Session.query(ImplantTemplate).filter(ImplantTemplate.cid == campaign_id).all()
        return self.db_methods._sqlalc_rows_to_list(sql_acl_obj)


    def get_implant_template(self, implant_template_id):
        pass
