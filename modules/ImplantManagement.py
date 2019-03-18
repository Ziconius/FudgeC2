from Database import Database
class ImplantManagement():
    db = Database()

    def ImplantCommandRegistration(self, cid , username, form):
        # -- This should be refactored at a later date to support read/write changes to
        # --    granular controls on templates, and later specific implants
        User = self.db.Verify_UserCanWriteCampaign(cid, username)
        if User == True:
            print("We can register commands")


        return

    def CreateNewImplant(self,cid,form, user):
        # -- This is creating a new Implant Template
        User = self.db.Get_UserObject(user)
        if User.admin == 0:
            return "Insufficient Priviledges"
        CampPriv = self.db.Verify_UserCanWriteCampaign(user,cid)
        if CampPriv == False:
            return "User cannot write to this campaign"
        # -- From here we know the user is able to write to the Campaign and an admin.

        try:
            print("SS")
            if "CreateImplant" in form:
                print("Inside subscript:",form)
                if form['title'] =="" or form['url'] =="" or form['description'] == "":
                    raise ValueError('Mandatory values left blank')
                title = form['title']
                url=form['url']
                port = form['port']
                description= form['description']
                beacon=form['beacon_delay']
                initial_delay=form['initial_delay']
                comms_http = 0
                comms_dns = 0
                comms_binary = 0
                if type(port) != int:
                    raise ValueError('Port is required as integer')
                # -- Comms check --#
                if "comms_http" in form :
                    comms_http = 1
                if "comms_dns" in form :
                    comms_dns = 1
                if "comms_binary" in form :
                    comms_binary = 1
                if comms_binary == 0 and comms_dns == 0 and comms_http ==0:
                    raise ValueError('No communitcation channel selected. ')
                a = self.db.Add_Implant(cid, title ,url,port,beacon,initial_delay,comms_http,comms_dns,comms_binary,description)
                if a == True:
                    return True
                else:
                    raise ValueError(str(a))
        except Exception as e:
            print("NewImplant: ",e)
            # -- Implicting returning page with Error --#
            return e