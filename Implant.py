class ImplantSingleton:
    class __OnlyOne:
        UID = None
        QueuedCommands = []
        CommandOutput = []
        # worth adding to the logging based on the commands issued here.
        def AddCommand(self, command):
            # Add record to issues command table with username - time - command - UID
            print("Adding CMD:",command)
            print("Current CMD list LEN:",len(self.QueuedCommands))
            self.QueuedCommands.append(command)

        def IssueCommand(self):
            if len(self.QueuedCommands) > 0:
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


x = ImplantSingleton()

