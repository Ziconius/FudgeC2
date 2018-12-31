#!/usr/bin/python3

import _thread
import time
import Implant
from Listener import app
import ImplantManager
# Define a function for the thread

# Evening -

def Start_Listener( threadName, delay):
    App.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000, threaded=True)

def Start_Controller(x,y):
   Manager.run(debug=True, use_reloader=False, host='0.0.0.0', port=5001, threaded=True)
   return


# Create two threads as follows
#Imp = Implant()
#Imp = Implant.Implant()
App = app #Listener
Manager= ImplantManager.app
Imp = Implant.ImplantSingleton.instance

try:
   _thread.start_new_thread( Start_Listener, ("Thread-1", 2, ) )
   _thread.start_new_thread( Start_Controller, ("Thread-1", 2,))
except:
   print ("Error: unable to start thread")
time.sleep(1)
while 1:

   a  =input("Please enter the command you would like to execute:")
   Imp.AddCommand(a)
   print("Commands awaiting execution: ",Imp.QueuedCommands)




