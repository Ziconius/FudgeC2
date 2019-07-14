import sys
import threading
import os


class Listener:

    def __init__(self, name, port, type):
        print("In Listener")
        self.name = name
        self.port = port
        self.type = type
        self.thread = None

    # def state_change(self, required_state):
    #     return
    def query_state(self):
        try:
            a = self.thread.is_alive()
        except Exception as E:
            a = False
        return a

    def stop_listener(self):
        self.thread = None


class HttpListener(Listener):
    pass
    # Read settings before this becomes an issue!
    tls_key = "server.key"
    tls_cert = "server.crt"
    path = os.getcwd() + "/Storage/"
    print(path)

    def create_app(self, listener_type):
        import FudgeC2.Listeners.HttpListener
        del sys.modules["FudgeC2.Listeners.HttpListener"]
        import FudgeC2.Listeners.HttpListener as HL
        HL.app.config['listener_type'] = listener_type
        return HL.app

    def start_http_listener_thread(self, obj, App, type):
        print(self.path + self.tls_cert)
        if type == "http":
            App.run(debug=False, use_reloader=False, host='0.0.0.0', port=obj, threaded=True)
        elif type == "https":
            App.run(debug=False, use_reloader=False, host='0.0.0.0', port=obj, threaded=True,
                    ssl_context=(self.path + self.tls_cert, self.path + self.tls_key))

    def start_listener(self):
        print("Running HTTP Listener: {}".format(self.port))
        a = self.create_app(self.type)
        self.thread = threading.Thread(target=self.start_http_listener_thread,
                                       args=(self.port, a, self.type,),
                                       daemon=True)
        self.thread.start()


class BinaryListener(Listener):
    pass

    def run(self):
        return



from FudgeC2.Data.Database import Database


class ListenerManagement:
    listeners = {}
    db = Database()

    def __init__(self, a, b):
        print(a, b)

    def _check_if_listener_is_unique(self, name, port, protocol):
        print("DATABASE: NOW CHECKING LISTENER IS COMPLETE")
        # self.db.listener.get_all_listeners()
        return True

    def _create_listener(self, name, protocol, port, auto_start=False):
        if self._check_if_listener_is_unique(name, port, protocol):
            if protocol == "http" or protocol == "https":
                self.listeners[name] = HttpListener(name, port, protocol)
            elif protocol == "binary":
                self.listeners['name'] = BinaryListener(name, port, protocol)
            else:
                return False
            self.db.listener.create_new_listener_record(name, port, protocol, auto_start)



    def _update_listener_state(self, listener, state):
        if listener in self.listeners.keys():
            if state == "off":
                print("turning listener off!")
                self.listeners[listener].stop_listener()
            elif state == "on":
                print("turning listener on!")
                self.listeners[listener].start_listener()
        return

    def check_tls_certificates(self):
        return True

    def get_active_listeners(self):
        blah = {}
        # if len(self.listeners) == 0:
        #     return {}
        for listener in self.listeners:
            # print(dir(self.listeners[listener]))
            blah[self.listeners[listener].name] = {"type":self.listeners[listener].type,
                                                   "port":self.listeners[listener].port,
                                                   "state":self.listeners[listener].query_state(),
                                                   "id":"who knows",
                                                   "common_name":self.listeners[listener].name}

        return blah


    # def process_for_submission(self, username, form):
    def listener_form_submission(self, username, form):
        if self.db.user.User_IsUserAdminAccount(username) is False:
            return False
        print(form)

        if "auto_start" in form:
            auto_start = False
            if "auto_start" in form:
                auto_start = True
            self._create_listener(form['name'], form['protocol'], form['port'],auto_start)


        elif "state_change" in form:
            print("we're now changing the state of a listener!!")
            if form['state_change'] in self.listeners.keys():
                current_state = self.listeners[form['state_change']].query_state()
                if current_state is True:
                    self._update_listener_state(form['state_change'], "off")
                else:
                    self._update_listener_state(form['state_change'], "on")

        else:
            return False, ""

        return True, ""