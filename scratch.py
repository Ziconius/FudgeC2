class ImplantSingleton:
    class __OnlyOne:

        UID = None
        QueuedCommands = []

        def AddCommand(self, command):
            # Add record to issues command table with username - time - command - UID
            self.QueuedCommands.append(command)

        def IssueCommand(self):
            if len(self.QueuedCommands) > 0:
                return self.QueuedCommands.pop()
            else:
                return "=="
    instance = None
    def __init__(self):
        if not ImplantSingleton.instance:
            ImplantSingleton.instance = ImplantSingleton.__OnlyOne()
        else:
            ImplantSingleton.instance.val = arg


x = ImplantSingleton()

