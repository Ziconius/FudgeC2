#!/usr/bin/python3
import _thread
import time
from Implant import Implant
from Listeners import HttpListener
from ServerApp import ImplantManager
from Storage.settings import Settings

# This will have to be ready to receive all HTTP requests, this will support ALL implants, and individual domains for C"
#   should be
#     controlled via Apache reverse proxies etc.


def start_listener():
    App.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000, threaded=True)


def start_controller():
    #  Using ssl_context as a temp measure, this should be changed in a production environment to support SSL via
    #  WSGI and NGINX.

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

# -- Build Database if none exists

try:
    _thread.start_new_thread(start_listener, ())
    _thread.start_new_thread(start_controller, ())
except Exception as E:
    print("Error: unable to start thread")
while 1:
    # Hold the application threads open
    time.sleep(10)
    pass
