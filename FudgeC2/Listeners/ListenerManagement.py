from Listeners import HttpListener
import _thread
from Data.Database import Database

class ListenerManagement():
    active_listener = 0
    listeners = {}
    db = Database()
    def listener_form_submission(self,user, form):
        # This will process the values submitted and decided what to call next
        #   these will require further management
        if not self.db.User_IsUserAdminAccount(user):
            return (False, "Insufficient privileges")
        # else:
        #     return (True, "Temp success value.")
        if 'state_change' in form:
            print("State change requested")
            if self.listeners[form['state_change']]['state'] == 0:
                print(form['state_change'])
                self.update_listener(form['state_change'],"start")
            elif self.listeners[form['state_change']]['state'] == 1:
                print(form['state_change'])
                self.update_listener(form['state_change'],"stop")
        elif 'listener_name' in form and 'listener_protocol' in form and 'listener_port' in form:
            print("Adding new implant")
            if 'auto_start' in form:
                auto_start = True
            else:
                auto_start = False
            a = self.create_listener(form['listener_name'], form['listener_protocol'].lower(), form['listener_port'],auto_start)
            return a

        return (True, "Placeholder content")


    def create_listener(self, listener_name, listener_type, port=None, auto_start=False, url=None):
        # Listener States:
        # 0 : Stopped
        # 1 : Running
        # 2 : Awaiting Stop
        # 3 : Awaiting Start
        a = self.__check_for_listener_duplicate_element(listener_name, "id")
        if a == False:
            return (False, "Existing listener name found")
        a = self.__check_for_listener_duplicate_element(port, "port")
        if a == False:
            return (False, "Existing port found")
        print(":::",a)
        print(listener_type, port, auto_start)
        if listener_type == "http" or listener_type == "https":
            if int(port):
                print("Creating: ", listener_type, port)
                # TODO: Likely bug prone
                id = "0000" + str(len(self.listeners))
                id = id[-4:]

                id = listener_name
                # --
                listener = {"type":listener_type, "port":port, "state":int(0), "id":id, "common_name":id}
                if auto_start == True:
                    listener["state"] = int(3)

                self.__validate_listener(listener)


                self.listeners[id] = listener
                if auto_start == True:
                    self.__review_listeners()
            else:
                print("port not int:", port)




        return (True, "Success")

    # User action
    def update_listener(self, id, action):
        print(id,action)
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
        for x in self.listeners.keys():
            print(self.listeners[x][key], "==",value)
            if self.listeners[x][key] == value:
                print(value, key)
                return False
        return True

    def __review_listeners(self):
        for l in self.listeners.keys():
            print("+",self.listeners[l])
            if int(self.listeners[l]['state']) == 2:
                print("state 2 found for ID:",l)
                self.__stop_listener(l)
            if int(self.listeners[l]['state']) == 3:
                self.__start_listener(l)


    def __start_listener(self, id):

        print("Starting: ", id)
        self.listeners[id]['state'] = 1

        if self.listeners[id]['type'] == "http":
            self.__start_http_listener(self.listeners[id])
        elif self.listeners[id]['type'] == "https":
            a = self.__start_https_listener(self.listeners[id])
            print("::",a)
        return
    def __stop_listener(self, id):
        print("Stopping: ", id)
        self.listeners[id]['state'] = 0
        return


    def __validate_listener(self, listener):
        # This will check for any conflicting arguments i.e. conflicting ports.

        return True


    # TODO: Refactor this code to remove as much code duplication.
    def __start_http_listener(self, obj):
        print("Pre-Thread",obj)
        self.listeners[obj['id']]['listener_thread'] = _thread.start_new_thread(self.start_http_listener_thread, (obj,))

    def __start_https_listener(self, obj):
        print("Pre-Thread",obj)
        _thread.start_new_thread(self.start_https_listener_thread, (obj,))

    def start_http_listener_thread(self, obj):
        App = HttpListener.app
        App.config['listener_type'] = "http"
        App.run(debug=True, use_reloader=False, host='0.0.0.0', port=obj['port'], threaded=True)

    def start_https_listener_thread(self, obj):
        AppSsl = HttpListener.app
        AppSsl.config['listener_type'] = "https"
        AppSsl.run(debug=True, use_reloader=False, host='0.0.0.0', port=obj['port'], threaded=True, ssl_context='adhoc')
