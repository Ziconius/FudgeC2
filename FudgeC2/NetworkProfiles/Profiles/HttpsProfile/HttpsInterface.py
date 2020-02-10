import os
import threading
import requests
from Storage.settings import Settings


class ListenerInterface:
    # Read settings before this becomes an issue!
    tls_key = f"{os.getcwd()}/Storage/{Settings.tls_listener_key}"
    tls_cert = f"{os.getcwd()}/Storage/{Settings.tls_listener_cert}"
    path = os.getcwd() + "/Storage/"
    app = None
    port = None
    thread = None

    def query_state(self):
        try:
            a = self.thread.is_alive()
        except Exception as E:
            a = False
        return a

    def configure(self, app, port):
        self.app = app.app
        self.port = port

    def _start_http_listener_thread(self):

        self.app.run(debug=False,
                     use_reloader=False,
                     host='0.0.0.0',
                     port=self.port,
                     threaded=True,
                     ssl_context=(self.tls_cert, self.tls_key))

    def start_listener(self):
        self.thread = threading.Thread(target=self._start_http_listener_thread,
                                       daemon=True)
        self.thread.start()

    # TODO: Randomise endpoint value.
    def stop_listener(self):
        try:
            requests.get(f"https://127.0.0.1:{self.port}/nlaksnfaobcaowb")
            self.thread = None
        except:
            print("Exception on HTTPS shutdown raised.")
