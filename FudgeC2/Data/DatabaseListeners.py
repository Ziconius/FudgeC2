from Data.models import Listeners


class DatabaseListener:

    def __init__(self, source_database, session):
        # TODO: Check session type
        self.Session = session
        self.db_methods = source_database

    def create_new_listener_record(self, name, port, protocol, auto_run):
        try:
            existing_listeners = self.get_all_listeners()
            for listener in existing_listeners:
                if listener['name'] == name:
                    return False
            new_listener = Listeners(name=name,
                                     state=0,
                                     protocol=protocol,
                                     port=port,
                                     auto_run=auto_run)
            self.Session.add(new_listener)
            self.Session.commit()

            return True
        except:
            return False

    def update_auto_run_state(self, listener_id, auto_run):
        # TODO: Allow listeners to have their auto_run value changed.
        return

    def get_all_listeners(self):
        rows = self.Session.query(Listeners).all()
        return self.db_methods._sqlalc_rows_to_list(rows)


    def get_listener_by_common_name(self, common_name):
        row = self.Session.query(Listeners).filter(Listeners.name == common_name).first()
        del row.__dict__['_sa_instance_state']
        row = row.__dict__
        return row
