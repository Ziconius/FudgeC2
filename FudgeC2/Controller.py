#!/usr/bin/python3
import _thread
import time
import os

from Storage.settings import Settings
from ServerApp import ImplantManager
from Listeners import ListenerManagement


def check_tls_certificates(cert, key):
    cert_result = os.path.isfile(os.getcwd() + "/Storage/" + cert)
    key_result = os.path.isfile(os.getcwd() + "/Storage/" + key)
    if key_result is False or cert_result is False:
        print("Warning: Missing crypto keys for TLS listeners. These will fail to boot.")
    return


def check_key_folders():
    # Placeholder for initialisation checking.
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
LM.start_auto_run_listeners_at_boot()

try:
    check_tls_certificates(Settings.tls_listener_cert, Settings.tls_listener_key)
    check_key_folders()
    _thread.start_new_thread(start_controller, (LM,))
except Exception as E:
    print("Error: Unable to start thread: ", E)
    exit()

while 1:
    # Hold the application threads open
    time.sleep(15)
    pass
