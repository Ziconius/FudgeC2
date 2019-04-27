import time
class log_test_dec():
    db = None
    wireframe = {
        "user":None,
        "campaign":None,
        "time":0,
        "log_type":None,
        "entry":None
    }
    def __init__(self, db_instance=0):
        self.db = db_instance


    def log_implant_activation(self, decorated_function):
        def decor_imp_act(*args, **kwargs):
            a = decorated_function(*args)
            return a
        return decor_imp_act



    def log_cmdreg(self, decorated_function):
        def decor_cmd_reg(*args, **kwargs):
            # print("decorator")
            a = decorated_function(*args,**kwargs)
            # print("::",*args)
            try:
                if a:
                    b = self.wireframe
                    b['user'] = args[1]
                    b['campaign'] = int(kwargs['cid'])
                    b['time'] = time.time()
                    b['log_type'] = "cmd_reg"
                    b['entry'] = {"cmd":args[3],"uik":args[2]}
                    # print(*args)
                    # print("~~",b)
                    args[0].Log_CampaignAction(b)
            except:
                pass
            return a
        return decor_cmd_reg

    def log_cmdpickup(self, decorated_function):
        def decor_cmd_pickup(*args, **kwargs):
            a = decorated_function(*args,**kwargs)
            if a:
                b=self.wireframe
                b['user']=args[1].uid
                b['campaign']=args[1].cid
                b['time']=time.time()
                b['log_type'] = "cmd_pickup"
                b['entry']={"cmd":args[1].log_entry,"uik":args[1].uik}
                # print(*args)
                args[0].Log_CampaignAction(b)
            return a
        return decor_cmd_pickup

    def log_cmdresponse(self, decorated_function):
        def decor_cmd_response(*args, **kwargs):
            a = decorated_function(*args,**kwargs)
            if a:
                b=self.wireframe
                b['user']=0
                b['campaign']=args[1]
                b['time']=time.time()
                b['log_type'] = "cmd_response"
                b['entry']={"uik":args[2],"response":args[3]}
                # print(*args)
                args[0].Log_CampaignAction(b)
            return a
        return decor_cmd_response