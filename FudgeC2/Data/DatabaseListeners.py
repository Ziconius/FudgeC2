from Data.models import ResponseLogs, Implants, ImplantLogs, Campaigns, CampaignUsers, GeneratedImplants, AppLogs, CampaignLogs, Users, Listeners


# DEV: This will be used to store records of listeners created within the FudgeC2 server instance.
#   Upon reboot/restart this will allow listeners to automatically restart.
class DatabaseListener:

    def __init__(self, source_database, session):
        # TODO: Check session type
        self.Session = session
        self.db_methods = source_database

    def create_new_listener_record(self, name, port, protocol, auto_run):

        print("def: create_new_listener_record")

        existing_listeners = self.get_all_listeners()
        for listener in existing_listeners:
            if listener.name == name:
                print("Listener exists")
                return False
        new_listener =  Listeners(name=name,
                                  state=0,
                                  protocol=protocol,
                                  port=port,
                                  auto_run=auto_run)
        self.Session.add(new_listener)
        self.Session.commit()

        return True

    def update_auto_state(self, listener_id, auto_run):
        return

    def get_all_listeners(self):
        a = self.Session.query(Listeners).all()
        return a

    def get_auto_run_listeners(self):
        a = self.Session.query(Listeners).filter(Listeners.auto_run == 1).all()
        return a
