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

        def AddCommand(self, User, Implant, Command):
            # -- Add record to issues command table with username - time - command - UID
            # -- Implement the logging calls to ensure entries got to DB. and get recorded on pick up

            # -- BUG: ENSURE THAT UID and IID are not confused.

            db.Register_ImplantCommand(User, Implant, Command)
            # print("--- Adding Command ---\nUser: ", User, "\nImplant:",Implant,"\nCommand:",Command)

            #IID=db.Get_ImplantFromKey(Implant)
            if  Implant not in self.RegisteredCommands:
                self.RegisteredCommands[Implant] = []
            self.RegisteredCommands[Implant].append(Command)

        def IssueCommand(self,IID=0):
            # print(IID)
            if IID != 0:
                # -- Issue command based on unique implant identifiers (UII)
                # -- UII is embedded into the implant via Jinja on delivery.
                ImplantObj=db.Get_ImplantFromKey(IID)
                # print(type(ImplantObj.iid),ImplantObj.iid)
                # print(self.RegisteredCommands)
                if ImplantObj.iid in self.RegisteredCommands:
                    if len(self.RegisteredCommands[ImplantObj.iid]) != 0:
                        a = self.RegisteredCommands[ImplantObj.iid].pop()
                        print(a)
                        return a

            # -- Create a suit null response.
            # --    This may be a random value, depending on how the implant handles it.
                return "=="
            else:
                return "=="
        def CommandResponse(self,result):
            print("Cmd Response Received:",result)
            print(type(result))
            aa = result.split("::", 1)
            print(aa)
            db.Register_ImplantResponse(aa[0],aa[1])
            # -- Legacy Format Below: To remove -- #
            self.CommandOutput.append(result)
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

