from Listeners import HttpListener
import _thread

class ListenerManagement():
    active_listener = 0
    listeners = {}


    def create_listener(self, listener_type, port=None, auto_start=False, url=None):
        # Listener States:
        # 0 : Stopped
        # 1 : Running
        # 2 : Awaiting Stop
        # 3 : Awaiting Start
        print(listener_type, port, auto_start)
        if listener_type == "http" or listener_type == "https":
            if int(port):
                print("Creating: ", listener_type, port)
                # TODO: Likely bug prone
                id = "0000" + str(len(self.listeners))
                id = id[-4:]
                # --
                listener = {"type":listener_type, "port":port, "state":int(0), "id":id, "common_name":"Blah: {}".format(id)}
                if auto_start == True:
                    listener["state"] = int(3)

                self.__validate_listener(listener)


                self.listeners[id] = listener
                if auto_start == True:
                    self.__review_listeners()
            else:
                print("port not int:", port)




        return

    # User action
    def update_listener(self, action, id):
        if action ==  "stop":
            self.listeners[id]["state"] = 2
        if action == "start":
            self.listeners[id]["state"] = 3
        self.__review_listeners()
        return

    # Review Data
    def get_active_listeners(self, type=None):
        return self.listeners




    def __review_listeners(self):
        # As this might be done twice in quick consession, there needs to be a locking mechanism.
        for l in self.listeners.keys():
            print(self.listeners[l])
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
            self.__start_https_listener(self.listeners[id])
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
        _thread.start_new_thread(self.start_http_listener_thread, (obj,))

    def __start_https_listener(self, obj):
        print("Pre-Thread",obj)
        _thread.start_new_thread(self.start_https_listener_thread, (obj,))

    def start_http_listener_thread(self, obj):
        App = HttpListener.app
        App.run(debug=True, use_reloader=False, host='0.0.0.0', port=obj['port'], threaded=True)

    def start_https_listener_thread(self, obj):
        App = HttpListener.app
        App.run(debug=True, use_reloader=False, host='0.0.0.0', port=obj['port'], threaded=True, ssl_context='adhoc')