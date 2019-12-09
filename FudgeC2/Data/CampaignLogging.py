import time


class CampaignLoggingDecorator:

    # TODO: Refactor variables to be more readable, improve commenting.
    db = None
    # LogType:
    #   new_imp
    #   cmd_reg
    #   cmd_pickup
    #   cmd_response
    wireframe = {
        "user": None,
        "campaign": None,
        "time": 0,
        "log_type": None,
        "entry": {}
    }

    def log_implant_activation(self, decorated_function):
        # TODO: Complete and test output
        def decor_imp_act(*args, **kwargs):
            a = decorated_function(*args, **kwargs)
            if a is not False:
                try:
                    b = self.wireframe
                    b['user'] = "0"
                    b['campaign'] = int(a[0]['cid'])
                    b['time'] = time.time()
                    b['log_type'] = "new_imp"
                    b['entry'] = {"stager_key": a[0]['stager_key'],
                                  "generated_title": a[0]['generated_title'],
                                  "callback_url": a[0]['callback_url'],
                                  "obfuscation_level": a[0]['obfuscation_level']
                                  }
                    args[0].db_methods.Log_CampaignAction(b)
                except Exception as e:
                    print(e)
                    pass
            return a
        return decor_imp_act

    def log_cmdreg(self, decorated_function):
        def decor_cmd_reg(*args, **kwargs):
            a = decorated_function(*args, **kwargs)
            try:
                if a:
                    b = self.wireframe
                    b['user'] = args[1]
                    b['campaign'] = int(kwargs['cid'])
                    b['time'] = time.time()
                    b['log_type'] = "cmd_reg"
                    b['entry'] = {"cmd": args[3],
                                  "uik": args[2]}
                    args[0].db_methods.Log_CampaignAction(b)
            except:
                pass
            return a
        return decor_cmd_reg

    def log_cmdpickup(self, decorated_function):
        def decor_cmd_pickup(*args, **kwargs):
            a = decorated_function(*args, **kwargs)
            if a:
                b = self.wireframe
                b['user'] = args[1].uid
                b['campaign'] = args[1].cid
                b['time'] = time.time()
                b['log_type'] = "cmd_pickup"
                b['entry'] = {"cmd": args[1].log_entry,
                              "uik": args[1].uik}
                args[0].db_methods.Log_CampaignAction(b)
            return a
        return decor_cmd_pickup


    # Due to changes this is now obsolete.
    def log_cmdresponse(self, decorated_function):
        def decor_cmd_response(*args, **kwargs):
            a = decorated_function(*args, **kwargs)
            if a:
                b = self.wireframe
                b['user'] = 0
                b['campaign'] = args[1]
                b['time'] = time.time()
                b['log_type'] = "cmd_response"
                b['entry'] = {"uik": args[1],
                              "response": args[2],
                              "c2_protocol": args[3]}
                args[0].db_methods.Log_CampaignAction(b)
            return a
        return decor_cmd_response

    # --
    # TODO: REVIEW AND COMPLETE
    # --
    # --
    def campaign_add_user(self, decorated_function):
        def decor_campaign_add_user(*args, **kwargs):
            a = decorated_function(*args, **kwargs)
            if a:
                b = self.wireframe
                b['user'] = args[2]
                b['campaign'] = args[1]
                b['time'] = time.time()
                b['log_type'] = "cmd_response"
                b['entry'] = {"campaign_title": args[1],
                              "permissions": args[3]}
                args[0].db_methods.Log_CampaignAction(b)
            return a
        return decor_campaign_add_user

    def campaign_modify_user_rights(self, decorated_function):
        def decor_campaign_modify_user_rights(*args, **kwargs):
            a = decorated_function(*args, **kwargs)
            # if statement checks that modify function returns true.
            if a:
                b = self.wireframe
                b['user'] = args[1]
                b['campaign'] = args[3]
                b['time'] = time.time()
                b['log_type'] = "campaign_user_modification"
                b['entry'] = {"permissions": args[2]}
                args[0].db_methods.Log_CampaignAction(b)
            return a
        return decor_campaign_modify_user_rights

    def new_implant_template_created(self, decorated_function):
        def decor_new_implant_template_created(*args, **kwargs):
            a = decorated_function(*args,**kwargs)
            # if statement checks that modify function returns true.
            if a:
                b = self.wireframe
                b['user'] = args[1]
                b['campaign'] = args[2]
                b['time'] = time.time()
                b['log_type'] = "new_implant_template"
                b['entry'] = {}
                for config_element in args[3]:
                    b['entry'][config_element] = args[3][config_element]
                # print(*args)
                args[0].db_methods.Log_CampaignAction(b)
            return a
        return decor_new_implant_template_created

    def update_implant_check_in(self, decorated_function):
        def decor_update_implant_check_in(*args, **kwargs):
            a = decorated_function(*args, **kwargs)
            # if statement checks that modify function returns true.
            if a:
                b = self.wireframe
                b['user'] = 0
                b['campaign'] = args[1]
                b['time'] = time.time()
                b['log_type'] = "implant_check_in"
                b['entry'] = {"unique_implant_id": args[2],
                              "c2_protocol": args[3]}

                args[0].db_methods.Log_CampaignAction(b)
            return a
        return decor_update_implant_check_in
