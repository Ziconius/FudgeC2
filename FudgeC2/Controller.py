#!/usr/bin/python3
import _thread
import time
from Implant import Implant
from Listeners import HttpListener
from ServerApp import ImplantManager
from Storage.settings import Settings
from Listeners import ListenerManagement



# This will have to be ready to receive all HTTP requests, this will support ALL implants, and individual domains for C"
#   should be
#     controlled via Apache reverse proxies etc.


def start_listener():
    App.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000, threaded=True)


def start_controller(LM):
    #  Using ssl_context as a temp measure, this should be changed in a production environment to support SSL via
    #  WSGI and NGINX.
    Manager.config['listener_management'] = LM
    Manager.run(debug=Settings.server_app_debug,
                use_reloader=False,
                host='0.0.0.0',
                port=Settings.server_app_port,
                threaded=True,
                ssl_context=Settings.server_app_ssl)
    return


# Create two threads as follows:
App = HttpListener.app  # Listener
Manager = ImplantManager.app
# Singleton in used to allow the app and the listeners to converse with implant object easily.
Imp = Implant.ImplantSingleton.instance
LM = ListenerManagement.ListenerManagement()


try:
    # _thread.start_new_thread(start_listener, ())
    _thread.start_new_thread(start_controller, (LM,))
except Exception as E:
    print("Error: unable to start thread", E)

# -- Hardcoding starting a listener on port 5000.
# --    This will be held here until a further testing, and implementing database support + autostart on reboot funcationality.
LM.create_listener("http",5000, True)

while 1:
    # Hold the application threads open
    time.sleep(15)
    LM.get_active_listeners()
    pass
