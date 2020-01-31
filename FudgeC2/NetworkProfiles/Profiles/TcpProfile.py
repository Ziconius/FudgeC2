class TcpProfile:
    name = "Basic TCP Profile"
    description = "This is a basic TCP network profile which encrypts all traffic using a symectric key"
    web_form_id = "TcpProfile"
    profile_tag = "TcpProfile"

    def get_powershell_code(self):
        a = '''
# This is test code!
function {{ ron.BasicTcpProfile }} (){
    Write-Host "Test BasicTcpProfile: port!: {{ ports.BasicTcpProfile_port }}  "
}
        '''
        return a

    def get_powershell_obf_strings(self):
        to_obf = {
            "BasicTcpProfile":"BasicTcpProfile_rnd"
        }
        port_number = {
            "BasicTcpProfile_port": None
        }
        return to_obf, port_number

    def get_powershell_implant_stager(self, implant_data=None):
        return None

    def get_docm_implant_stager(self, implant=None):
        return None

    def get_webform(self):
        a = '''
<div class="checkbox">
    <label><input type="checkbox" name="BasicHttpProfile" value="off"> TCP Profile</label>
    <input type="text" class="form-control" id="TcpProfile" name="TcpProfile" placeholder="TCP Port for binary listener">
</div>

'''
        return a

    def validate_web_form(self, key,  value):
        try:
            if int(value) > 0 and int(value) < 65355:
                return {self.web_form_id: int(value)}
            else:
                return False
        except:
            return False


    def get_listener_profile_form(self):
         #a = "<p>hello world this is the TCP profile form</p>"
        a = {"name": self.name,
             "profile_tag": self.profile_tag,
             "port": "Port"}
        return a