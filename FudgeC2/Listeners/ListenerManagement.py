import sys
import _thread
import os
from FudgeC2.Data.Database import Database

class ListenerManagement():
    # TODO: Add checks for failed/failing listeners (i.e. certs not configured & thread dies.)
    active_listener = 0
    listeners = {}
    db = Database()
    tls_cert = None
    tls_key = None
    def __init__(self, tls_listener_cert, tls_listener_key):
        # TODO: Implement checks to validate files at this point.
        self.tls_cert = tls_listener_cert
        self.tls_key = tls_listener_key

    def check_tls_certificates(self):
        cert_result = os.path.isfile(os.getcwd() + "/Storage/" + self.tls_cert)
        key_result = os.path.isfile(os.getcwd() + "/Storage/" + self.tls_key)
        if key_result is False or cert_result is False:
            print("Warning: ListenerManagement.check_tls_certificates() has failed. Generate certificates.")
            return False
        else:
            return True

    def create_listener(self, listener_name, listener_type, port=None, auto_start=False, url=None):
        # Listener States:
        # 0 : Stopped
        # 1 : Running
        # 2 : Awaiting Stop
        # 3 : Awaiting Start
        supported_listeners = ["http", "https"]
        a = self.__check_for_listener_duplicate_element(listener_name, "common_name")
        if a == False:
            return (False, "Existing listener name found.")
        a = self.__check_for_listener_duplicate_element(port, "port")
        if a == False:
            return (False, "Existing port found.")


        if listener_type in supported_listeners:
            if int(port):


                # TODO: Likely to contain bugs if deletion is implemented?
                id = "0000" + str(len(self.listeners))
                id = id[-4:]


                # --
                listener = {"type":listener_type, "port":port, "state":int(0), "id":id, "common_name":listener_name}
                if auto_start == True:
                    listener["state"] = int(3)

                self.__validate_listener(listener)
                self.listeners[id] = listener

                if auto_start == True:
                    self.__review_listeners()
            else:
                return(False, "Please submit the port as an integer.")
            return(False, "Invalid listener configuration.")
        return (True, "Success")

    def listener_form_submission(self,user, form):
        # This will process the values submitted and decided what to call next
        #   these will require further management
        if not self.db.user.User_IsUserAdminAccount(user):
            return (False, "Insufficient privileges")
        # else:
        #     return (True, "Temp success value.")
        if 'state_change' in form:
            # print("State change requested")
            if self.listeners[form['state_change']]['state'] == 0:
                # print(form['state_change'])
                self.update_listener(form['state_change'],"start")
            elif self.listeners[form['state_change']]['state'] == 1:
                # print(form['state_change'])
                self.update_listener(form['state_change'],"stop")

        elif 'listener_name' in form and 'listener_protocol' in form and 'listener_port' in form:
            # print("Adding new listener")
            if 'auto_start' in form:
                auto_start = True
            else:
                auto_start = False
            a = self.create_listener(form['listener_name'], form['listener_protocol'].lower(), form['listener_port'],auto_start)
            return a

        return (True, "Implant started sucessfully.")

    # User action
    def update_listener(self, id, action):
        # print(id,action)
        if action ==  "stop":
            self.listeners[id]["state"] = 2
        if action == "start":
            self.listeners[id]["state"] = 3
        self.__review_listeners()
        return

    # Review Data
    def get_active_listeners(self, type=None):
        return self.listeners

    def __check_for_listener_duplicate_element(self, value, key):
        for listener_id in self.listeners.keys():
            if self.listeners[listener_id][key] == value:
                print(value, key)
                return False
        return True

    def __review_listeners(self):
        for listener_id in self.listeners.keys():
            if int(self.listeners[listener_id]['state']) == 2:
                self.__stop_listener(listener_id)
            if int(self.listeners[listener_id]['state']) == 3:
                self.__start_listener(listener_id)

    def __start_listener(self, id):
        self.listeners[id]['state'] = 1
        if self.listeners[id]['type'] == "http":
            self.__start_http_listener(self.listeners[id])
        elif self.listeners[id]['type'] == "https":
            self.__start_https_listener(self.listeners[id])
        elif self.listeners[id]['type'] == "dns":
            self.__start_dns_listener(self.listeners[id])
        return

    def __stop_listener(self, id):
        self.listeners[id]['state'] = 0
        return

    def __validate_listener(self, listener):
        # This will check for any conflicting arguments i.e. conflicting ports.
        return True

    # TODO: Refactor this code to remove as much code duplication.
    def __start_http_listener(self, obj):
        flask_listener_object = self.create_app("http")
        self.listeners[obj['id']]['listener_thread'] = _thread.start_new_thread(self.start_http_listener_thread, (obj, flask_listener_object, ))

    def __start_https_listener(self, obj):
        flask_listener_object = self.create_app("https")
        self.listeners[obj['id']]['listener_thread'] = _thread.start_new_thread(self.start_https_listener_thread, (obj, flask_listener_object, ))

    def __start_dns_listener(self, obj):
        # -- This listener is not implemented yet.
        return

    def __start_binary_listener(self, obj):
        # -- This listener is not implemented yet.
        return

    def create_app(self, listener_type):
        import FudgeC2.Listeners.HttpListener
        del sys.modules["FudgeC2.Listeners.HttpListener"]
        import FudgeC2.Listeners.HttpListener as HL
        HL.app.config['listener_type'] = listener_type
        return HL.app

    def start_http_listener_thread(self, obj, App):
        App.run(debug=False, use_reloader=False, host='0.0.0.0', port=obj['port'], threaded=True)

    def start_https_listener_thread(self, obj, App):
        path = os.getcwd()+"/Storage/"
        if self.check_tls_certificates():
            App.run(debug=False, use_reloader=False, host='0.0.0.0', port=obj['port'], threaded=True, ssl_context=(path+self.tls_cert, path+self.tls_key))
        else:
            print()
            # -- User has not set up certificates in the Storage dir
            return False