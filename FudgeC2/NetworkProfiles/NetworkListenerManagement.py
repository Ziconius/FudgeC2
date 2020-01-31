from NetworkProfiles.NetworkProfileManager import NetworkProfileManager
from Data.Database import Database


class NetworkListenerManagement:
    class __OnlyOne:
        # Transition notes: This is class considered complete and functional.
        # Dev Work:
        #   Improve logging on listener events
        #   Improve race-condition checks
        #   Rework and rename 'protocol' as a word to 'profile_tag' to match network profile terminology

        listeners = []
        db = Database()
        npm = NetworkProfileManager()

        def create_new_listener(self, username, common_name, profile_tag, args, auto_start):
            # First check the profile tag is valid, and then ensure adding the listener to the DB is successful
            #   before taking action.
            if self.db.user.User_IsUserAdminAccount(username):
                listener_class = self.npm.get_listener_object(profile_tag)
                listener_interface = self.npm.get_listener_interface(profile_tag)
                if listener_class is not None and listener_interface is not None:

                    if self.db.listener.create_new_listener_record(common_name, args, profile_tag, auto_start):
                        listener = self.db.listener.get_listener_by_common_name(common_name)
                        if listener is not False:
                            print(listener)
                            # already instantiated interface
                            listener['interface'] = listener_interface
                            listener['interface'].configure(listener_class, args)
                            self.listeners.append(listener)
                            self.listener_state_change(username, listener['name'], listener['auto_run'])
            return False

        def get_all_listeners(self):
            return self.listeners

        def get_listener_state(self, common_name):
            for listener in self.listeners:
                if listener['common_name'] == common_name:
                    return listener['object'].query_state()

        def startup_auto_run_listeners(self):
            tmp_listeners = self.db.listener.get_all_listeners()
            for listener in tmp_listeners:
                listener_class = self.npm.get_listener_object(listener['protocol'])
                listener_interface = self.npm.get_listener_interface(listener['protocol'])
                if listener_class is not None and listener_interface is not None:

                    # Already instantiated interface
                    listener['interface'] = listener_interface
                    listener['interface'].configure(listener_class, listener['port'])
                    self.listeners.append(listener)
                    self.listener_state_change(True, listener['name'], listener['auto_run'])

        def listener_state_change(self, username, common_name, state):
            state_change_message = "Insufficient privileges"
            if self.db.user.User_IsUserAdminAccount(username) or username is True:
                for listener in self.listeners:
                    if listener['name'] == common_name:
                        if state == 0 and listener['state'] == 1:
                            listener['state'] = 0
                            listener['interface'].stop_listener()
                            state_change_message = f"Successfully stopped {common_name}"
                        elif state == 1:
                            listener['state'] = 1
                            listener['interface'].start_listener()
                            state_change_message = f"Successfully started {common_name}"
            return False, state_change_message

        # Undecided if I want to check for server certificates at a global level - this should be down to
        #   specific network profiles?
        # Note: This is still called when the C2 server starts for now so automatically return True.
        @staticmethod
        def check_tls_certificates():
            return True

    instance = None

    def __init__(self):
        if not NetworkListenerManagement.instance:
            NetworkListenerManagement.instance = NetworkListenerManagement.__OnlyOne()
        else:
            NetworkListenerManagement.instance.val = arg


NetworkListenerManagement()
