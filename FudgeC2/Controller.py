#!/usr/bin/python3
import _thread
import time
from Implant import Implant
from ServerApp import ImplantManager
from Storage.settings import Settings
from Listeners import ListenerManagement


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


# Singleton in used to allow the app and the listeners to converse with implant object easily.
Imp = Implant.ImplantSingleton.instance
Manager = ImplantManager.app
LM = ListenerManagement.ListenerManagement()

# -- Hardcoding a listener on port 5000.
# --    This will be held here until a further testing, and implementing database support + autostart on reboot
# --    functionality. Passing in the user "admin" which as a hardcoded value. If 'admin' if not a real admin
# --    account this will fail.
LM.create_listener("hardcoded http listener", "http",5000, True)
LM.create_listener("hardcoded https listener", "https",8080)

try:
    _thread.start_new_thread(start_controller, (LM,))
except Exception as E:
    print("Error: Unable to start thread: ", E)
    exit()


while 1:
    # Hold the application threads open
    time.sleep(15)
    # LM.get_active_listeners()
    pass
