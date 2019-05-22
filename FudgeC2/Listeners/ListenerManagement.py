class ListenerManagement():
    active_listener = 0
    # {"http":[]}
    listeners = {
        "http"   : [],
        "https"  : [],
        "dns"    : [],
        "binary" : []
    }
    def start_listener(self, listener_type, port=None, url=None):
        if listener_type == "http" or listener_type == "https":
            if int(port):
                print("Starting: ", listener_type, port)
        return
    def get_active_listeners(self, type=None):

        return self.listeners
    def awaiting_start(self):
        print("awaiting: ",self.active_listener)
        return
    def stop_listener(self):
        return
    def awaiting_stop(self):
        return