#!/usr/bin/python3
import _thread
import time
import os

from FudgeC2.Storage.settings import Settings
from FudgeC2.ServerApp import ImplantManager
from FudgeC2.Listeners import ListenerManagement


def check_tls_certificates(cert, key):
    cert_result = os.path.isfile(os.getcwd() + "/Storage/" + cert)
    key_result = os.path.isfile(os.getcwd() + "/Storage/" + key)
    if key_result is False or cert_result is False:
        print("Warning: Missing crypto keys for TLS listeners. These will fail to boot.")
    return


def start_controller(listener_management):
    # Server configuration can be found in Storage/settings.py
    Manager.config['listener_management'] = listener_management
    Manager.run(debug=Settings.server_app_debug,
                use_reloader=False,
                host='0.0.0.0',
                port=Settings.server_app_port,
                threaded=True,
                ssl_context=Settings.server_app_ssl)
    return


Manager = ImplantManager.app
LM = ListenerManagement.ListenerManagement(Settings.tls_listener_cert, Settings.tls_listener_key)

# -- Hard coding a listener on port 5000 & 8080.
# --    This will be held here until a further testing, and implementing database support + auto start on reboot
# --    functionality. Passing in the user "admin" which as a hardcoded value.
# --
# --    Note: If 'admin' if not a existing admin account this will fail.
LM.create_listener("hardcoded http listener", "http", 5000, False)
LM.create_listener("hardcoded https listener", "https", 8080, False)  # This requires TLS certs before starting.
# LM.create_listener("hardcoded https listener 2", "http",1234, True)

try:
    check_tls_certificates(Settings.tls_listener_cert, Settings.tls_listener_key)
    _thread.start_new_thread(start_controller, (LM,))
except Exception as E:
    print("Error: Unable to start thread: ", E)
    exit()

while 1:
    # Hold the application threads open
    time.sleep(15)
    pass
