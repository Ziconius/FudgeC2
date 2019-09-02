import time
import random
from Data.models import ResponseLogs, Implants, ImplantLogs, Campaigns, CampaignUsers, GeneratedImplants
# AppLogs, CampaignLogs, Users
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
                                            Implants).filter(Implants.iid == GeneratedImplants.iid,
                                                             GeneratedImplants.generated_title == implant_title).all()

        implant_object = self.db_methods.__splice_implants_and_generated_implants__(implant_object)
        return implant_object

    # TODO: Add logging
    @CL.new_implant_template_created
    def create_new_implant_template(self, user, cid, config):

        stager_key = random.randint(10000, 99999)
        new_implant = Implants(
            cid=cid,
            title=config['title'],
            description=config['description'],
            stager_key=stager_key,
            callback_url=config['url'],
            beacon=config['beacon'],
            initial_delay=config['initial_delay'],
            obfuscation_level=config['obfuscation_level'],
            comms_http=config['protocol']['comms_http'],
            comms_https=config['protocol']['comms_https'],
            comms_binary=config['protocol']['comms_binary'],
            comms_dns=config['protocol']['comms_dns']
        )
        self.Session.add(new_implant)
        try:
            self.Session.commit()
            self.Session.query(Implants).first()
            return True

        except Exception as e:
            print("db.Add_Implant: ", e)
            return e

    def Get_AllImplantBaseFromCid(self, cid):
        # -- THIS NEED TO BE REBUILT
        all_implants = self.Session.query(Implants).filter(Implants.cid == cid).all()
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
        print(campaign_id)
        raw_implants = self.Session.query(GeneratedImplants,
                                          Implants).filter(GeneratedImplants.iid == Implants.iid,
                                                           Implants.cid == campaign_id).all()
        print(raw_implants)
        generated_implants = self.db_methods.__splice_implants_and_generated_implants__(raw_implants)
        if generated_implants is not None:
            return generated_implants
        else:
            return False

    def Get_GeneratedImplantDataFromUIK(self, UIK):
        # -- Pulls all configuration data for a generated implant based on UIK.
        # --    Used when implants checks in.
        result = self.Session.query(GeneratedImplants, Implants).filter(Implants.iid == GeneratedImplants.iid,
                                                                        GeneratedImplants.unique_implant_id == UIK
                                                                        ).first()

        implant_list = self.db_methods.__splice_implants_and_generated_implants__(result)
        for implant_template in implant_list:
            if '_sa_instance_state' in implant_template:
                del implant_template['_sa_instance_state']

        if implant_list is not None:
            return implant_list[0]
        else:
            return False

    @CL.log_implant_activation
    def Register_NewImplantFromStagerKey(self, stager_key):
        # -- We are registering a NEW implant and generating a unique_stager_key (or UIK)
        # -- Moving forward all reference to ImplantKey/UII should be changed to StagerID

        implant = self.Session.query(Implants).filter(Implants.stager_key == stager_key).first()
        if implant is not None:
            unique_implant_key = random.randint(000000, 999999)
            new_title = str(implant.title) + "_" + str(unique_implant_key)
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

            active_implant_record = self.Session.query(GeneratedImplants, Implants).filter(
                Implants.iid == GeneratedImplants.iid,
                GeneratedImplants.unique_implant_id == unique_implant_key).first()

            active_implant_record = self.db_methods.__splice_implants_and_generated_implants__(active_implant_record)
            print("Post splicechecl: ", active_implant_record)
            # -- Return Raw objects, and caller to manage them,
            return active_implant_record
        return False

    def Set_GeneratedImplantCopy(self, new_spliced_implant_data, generated_implant):
        # This will store a copy of the PS implant to the "Generated_Implants" table
        #   This will allow RT to send analysable copy to BT for signaturing etc.
        try:
            uik = new_spliced_implant_data['unique_implant_id']
            self.Session.query(GeneratedImplants).filter(
                GeneratedImplants.unique_implant_id == uik).update({"implant_copy": generated_implant})

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
                                    Implants,
                                    GeneratedImplants
                                    ).filter(
                            CampaignUsers.uid == uid,
                            Campaigns.cid == CampaignUsers.cid,
                            Implants.cid == Campaigns.cid,
                            Implants.iid == GeneratedImplants.iid,
                            GeneratedImplants.unique_implant_id == uik).all()

        if len(result) == 0:
            print("No Implant <--> User association")
            return False
        for line in result:
            if line[0].permissions == 2:
                cid = line[0].cid
                new_implant_log = ImplantLogs(cid=cid,
                                              uid=uid,
                                              time=time.time(),
                                              log_entry=command,
                                              uik=uik,
                                              read_by_implant=0)

                self.Session.add(new_implant_log)
                try:
                    self.Session.commit()
                    self.Session.query(ImplantLogs).first()
                    return True
                except Exception as e:
                    print("db.Register_ImplantCommand: ", e)
                    return False
            else:
                # -- Incase non 0/1 response --#
                return False

    def Get_RegisteredImplantCommandsFromUIK(self, unique_implant_key):
        # -- Return List
        logs = self.Session.query(ImplantLogs).filter(ImplantLogs.uik == unique_implant_key).all()
        if logs is not None:
            return logs
        else:
            return []

    def Get_RegisteredImplantCommandsFromCID(self, campaign_id):
        # Used by web app.
        logs = self.Session.query(ImplantLogs).filter(ImplantLogs.cid == campaign_id).all()
        if len(logs) > 0:
            return logs
        else:
            return []

    @CL.log_cmdpickup
    def Register_ImplantCommandPickup(self, record, protocol):
        self.Session.query(ImplantLogs).filter(
            ImplantLogs.uik == record.uik,
            ImplantLogs.log_entry == record.log_entry,
            ImplantLogs.time == record.time).update({'read_by_implant': int(time.time()), 'c2_protocol': str(protocol)})
        try:
            self.Session.commit()
            return True
        except Exception as E:
            print("Exception: ", E)
            return False

    @CL.log_cmdresponse
    def Register_ImplantResponse(self, cid, unique_implant_id, response, c2_protocol):
        # -- TODO: REBUILD
        # Pull back the first record which matches the UIK, contain both the Campaign the IID
        #   is associated from the implant the UIk is associated with.
        info = self.Session.query(Implants, Campaigns, GeneratedImplants).filter(
            Campaigns.cid == Implants.cid).filter(
            Implants.iid == GeneratedImplants.iid).filter(GeneratedImplants.unique_implant_id == unique_implant_id).first()
        iid = info[0].iid
        cid = info[1].cid
        uik = info[2].unique_implant_id
        if response == "":
            print("Registering empty response.")
            return False
        response_logs = ResponseLogs(cid=cid, uik=uik, log_entry=response, time=int(time.time()))
        self.Session.add(response_logs)
        try:
            self.Session.commit()
            return True
        except Exception as E:
            print(E)

    def Get_CampaignImplantResponses(self, cid):
        # Used by web app
        # -- TODO: Refactor
        a = self.Session.query(ResponseLogs).filter(ResponseLogs.cid == cid).all()
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
