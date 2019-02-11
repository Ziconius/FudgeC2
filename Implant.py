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
            # Add record to issues command table with username - time - command - UID
            # Implement the logging calls to ensure entries got to DB. and get recorded on pick up
            print("Adding CMD:",Command)
            db.Register_ImplantCommand(User, Implant, Command)
            # -- REMOVE: BELOW
            self.QueuedCommands.append(Command)

            if  Implant not in self.RegisteredCommands:
                self.RegisteredCommands[Implant] = []
                # print("Implant not in dict")
            self.RegisteredCommands[Implant].append(Command)
            # print(self.RegisteredCommands[Implant])
            print("Current CMD list LEN:", len(self.QueuedCommands))

        def IssueCommand(self,IID=0):
            if len(self.QueuedCommands) > 0:
                # -- Issue command based on unique implant identifiers (UII)
                # -- UII is embedded into the implant via Jinja on delivery.
                db.Get_ImplantKey(IID)
                if IID not in self.RegisteredCommands:
                    a = self.RegisteredCommands['IID'].pop()
                return self.QueuedCommands.pop()
            else:
                return "=="
        def CommandResponse(self,result):
            self.CommandOutput.append(result)
            return 0

        def Get_CommandResult(self):
            #print("cmdres:",len(self.CommandOutput))
            return self.CommandOutput

    instance = None
    def __init__(self):
        if not ImplantSingleton.instance:
            ImplantSingleton.instance = ImplantSingleton.__OnlyOne()
        else:
            ImplantSingleton.instance.val = arg

db = Database()
x = ImplantSingleton()

