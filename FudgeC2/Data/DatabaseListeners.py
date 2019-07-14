from FudgeC2.Data.models import ResponseLogs, Implants, ImplantLogs, Campaigns, CampaignUsers, GeneratedImplants, AppLogs, CampaignLogs, Users

class DatabaseListener:

    def __init__(self, source_database, session):
        # TODO: Check session type
        self.Session = session
        self.db_methods = source_database

    def create_new_listener_record(self, a, b, c, d):
        print("Now in DB: create_new_listener_record")
        return
