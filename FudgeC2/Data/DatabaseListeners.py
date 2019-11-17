from Data.models import Listeners


class DatabaseListener:

    def __init__(self, source_database, session):
        # TODO: Check session type
        self.Session = session
        self.db_methods = source_database

    def create_new_listener_record(self, name, port, protocol, auto_run):

        existing_listeners = self.get_all_listeners()
        for listener in existing_listeners:
            if listener.name == name:
                return False
        new_listener = Listeners(name=name,
                                 state=0,
                                 protocol=protocol,
                                 port=port,
                                 auto_run=auto_run)
        self.Session.add(new_listener)
        self.Session.commit()

        return True

    def update_auto_run_state(self, listener_id, auto_run):
        # TODO: Allow listeners to have their auto_run value changed.
        return

    def get_all_listeners(self):
        return self.Session.query(Listeners).all()

    def get_auto_run_listeners(self):
        return self.Session.query(Listeners).filter(Listeners.auto_run == 1).all()
