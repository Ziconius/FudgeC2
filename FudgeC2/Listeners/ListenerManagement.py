import sys
import threading
import os
import requests

from Data.Database import Database


class Listener:

    def __init__(self, name, port, type):
        # print("In Listener")
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
    # print(path)

    # Internal
    def create_app(self, listener_type):
        import Listeners.HttpListener
        del sys.modules["Listeners.HttpListener"]
        import Listeners.HttpListener as http_listener_module
        http_listener_module.app.config['listener_type'] = listener_type
        return http_listener_module.app

    # Internal
    def start_http_listener_thread(self, obj, App, protocol_type):
        # print(self.path + self.tls_cert)
        if protocol_type == "http":
            App.run(debug=False, use_reloader=False, host='0.0.0.0', port=obj, threaded=True)
        elif protocol_type == "https":
            App.run(debug=False,
                    use_reloader=False,
                    host='0.0.0.0',
                    port=obj,
                    threaded=True,
                    ssl_context=(self.path + self.tls_cert, self.path + self.tls_key))

    # External
    def start_listener(self):
        print("name: {}, port: {}, proto: {}".format(self.name,self.port,self.type))
        print("Running HTTP Listener: {}".format(self.port))
        app = self.create_app(self.type)
        self.thread = threading.Thread(target=self.start_http_listener_thread,
                                       args=(self.port, app, self.type,),
                                       daemon=True)
        self.thread.start()

    # External
    # TODO: Randomise endpoint value.
    def stop_listener(self):
        requests.get("{}://127.0.0.1:{}/nlaksnfaobcaowb".format(self.type, self.port))
        self.thread = None


class BinaryListener(Listener):
    pass

    def run(self):
        return



class ListenerManagement:
    listeners = {}
    db = Database()

    def __init__(self, a, b):
        # print(a, b)
        pass

    def _check_if_listener_is_unique(self, name, port, protocol):
        # print("DATABASE: NOW CHECKING LISTENER IS COMPLETE")
        # self.db.listener.get_all_listeners()
        return True

    def _create_listener(self, name, raw_protocol, port, auto_start=False, reboot=False):
        protocol = raw_protocol.lower()
        if self._check_if_listener_is_unique(name, port, protocol):
            if protocol.lower() == "http" or protocol.lower() == "https":
                self.listeners[name] = HttpListener(name, port, protocol)
            elif protocol == "binary":
                self.listeners['name'] = BinaryListener(name, port, protocol)
            else:
                return False

            if reboot is not True:
                if self.db.listener.create_new_listener_record(name, port, protocol, auto_start) is False:
                    return False

            if auto_start == True:
                self.listeners[name].start_listener()


        else:
            print("name not unique.")
            return False

        return True


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
            blah[self.listeners[listener].name] = {"type": self.listeners[listener].type,
                                                   "port": self.listeners[listener].port,
                                                   "state": self.listeners[listener].query_state(),
                                                   "id": "who knows",
                                                   "common_name": self.listeners[listener].name}

        return blah


    # def process_for_submission(self, username, form):
    def listener_form_submission(self, username, form):
        if self.db.user.User_IsUserAdminAccount(username) is False:
            return False, "You are not an admin."
        # print(form)

        if "listener_name" in form:
            auto_start = False
            if "auto_start" in form:
                auto_start = True
            listener_created = self._create_listener(form['listener_name'], form['listener_protocol'], form['listener_port'],auto_start)
            if listener_created is True:
                return True, "Listener created"
            else:
                return False, "Error in _create_listener()"

        elif "state_change" in form:
            # print("we're now changing the state of a listener!!")
            if form['state_change'] in self.listeners.keys():
                current_state = self.listeners[form['state_change']].query_state()
                if current_state is True:
                    self._update_listener_state(form['state_change'], "off")
                else:
                    self._update_listener_state(form['state_change'], "on")

        else:
            return False, ""

        return True, ""

    def start_auto_run_listeners_at_boot(self):
        auto_run_listeners = self.db.listener.get_all_listeners()
        for listener in auto_run_listeners:
            self._create_listener(listener.name, listener.protocol, listener.port, listener.auto_run, True)
