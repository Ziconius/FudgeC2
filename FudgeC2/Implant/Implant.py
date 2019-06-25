from FudgeC2.Data.Database import Database
from FudgeC2.Implant.ImplantGenerator import ImplantGenerator

class ImplantSingleton:
    class __OnlyOne:
        # -- The Implant class is sole class responsible for controlling data to and from implants.
        # --    it manages  these interaction across all types of implants and communication protocols.

        def AddCommand(self, User, cid, UniqueImplantKey,Command):
            # AddCommand is responsible for creating new entries for implants to pickup.
            #   User validation checks must occur before a command is registered.
            db.Register_ImplantCommand(User, UniqueImplantKey, Command, cid=cid)


        def IssueCommand(self,UIK=0, c2_protocol=None):
            if UIK != 0:
                # -- Issue command based on unique implant identifiers (UIK)
                # -- UIK is embedded into the implant via Jinja on delivery.

                # Updates an implants last check-in time.
                db.Update_ImplantLastCheckIn(UIK, c2_protocol)

                ImplantObj=db.Get_GeneratedImplantDataFromUIK(UIK)
                for implant in ImplantObj:
                    ImpLogs = db.Get_RegisteredImplantCommandsFromUIK(implant['unique_implant_id'])
                    tmpImpLogs = []
                    for x in ImpLogs:
                        if x.read_by_implant == 0:
                            tmpImpLogs.append(x)
                    if len(tmpImpLogs) != 0:
                        Entry = min(tmpImpLogs, key=lambda x: x.time)
                        if db.Register_ImplantCommandPickup(Entry, c2_protocol):
                            return Entry.log_entry

            # -- Create a suitable null response.
            # --    This may be a random value, depending on how the implant handles it.
                return "=="
            else:
                return "=="

        # -- Used by Implant - Logs command responses from infected machines.
        def CommandResponse(self,unique_implant_key , cmd_result, c2_protocol=None):
            generated_implant_data = db.Get_GeneratedImplantDataFromUIK(unique_implant_key)
            db.Register_ImplantResponse(generated_implant_data[0]['cid'],unique_implant_key,cmd_result, c2_protocol)


        # -- Used by webapp.
        def Get_CommandResult(self,cid):
            # -- This trust any calls have already been authenticated/
            # --    May need to move authentication to this level.
            return db.Get_CampaignImplantResponses(cid)

        # -- Used by Implant stagers to create a suitable implant based on implant template configuration
        def GeneratePayload(self, NewSplicedImplantData):
            # -- Refactor code: variable names + checks on types.
            ImpGen = ImplantGenerator()
            if len(NewSplicedImplantData) == 1:
                NewSplicedImplantData = NewSplicedImplantData[0]
            rendered_implant = ImpGen.generate_implant_from_template(NewSplicedImplantData)
            db.Set_GeneratedImplantCopy(NewSplicedImplantData, rendered_implant)
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
