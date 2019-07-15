from Data.models import ResponseLogs, Implants, ImplantLogs, Campaigns, CampaignUsers, GeneratedImplants, AppLogs, CampaignLogs, Users


# DEV: This will be used to store records of listeners created within the FudgeC2 server instance.
#   Upon reboot/restart this will allow listeners to automatically restart.
class DatabaseListener:

    def __init__(self, source_database, session):
        # TODO: Check session type
        self.Session = session
        self.db_methods = source_database

    def create_new_listener_record(self, a, b, c, d):
        # print("Now in DB: create_new_listener_record")
        return
