import base64
import os


class PlayAudio:
    type = "PS"
    args = "Local sound file location"
    input = "play_audio"

    def process_implant_response(self, data, args):
        if data.decode()=="1":
            return f"Audio success: {args}", None
        else:
            return f"Audio play failed.", None

    def implant_text(self):
        var = '''
function {{ ron.obf_remote_play_audio }}($data){
    if ($data.length -lt 4){
            $global:tr = 0
        }
    $wshShell = new-object -com wscript.shell;1..50  | % {$wshShell.SendKeys([char]175)}
    $fs = [System.IO.MemoryStream]::new($data)
    $PlayWav = [System.Media.SoundPlayer]::new($fs)
    $PlayWav.play()
    $PlayWav.Dispose()
    $global:tr = 1
}
'''
        return var

    def pre_process_command(self, argument_string):
        # Check if the argument to be passed to the implant is valid.
        # I.e.
        #    Does the file to be uploaded exist local?
        #    Is the command to be executed dangerous?
        # Check file extension for ".wav"
        path = f"{os.getcwd()}/Storage/implant_resources/{argument_string}"
        print(path)
        file_exists = os.path.exists(path)
        print(file_exists)
        if file_exists:
            return True
        else:
            return f"WAV file does not exist: {path}"
        # return True

    def create_module_data_string(self, cmd_entry):
        # This function is responsible for creating the string which is send to the implant
        # Format for the implant core string is:
        #   < command type > <command id><optional command arguments>

        path = f"{os.getcwd()}/Storage/implant_resources/{cmd_entry['args']}"
        with open(path, 'rb') as file:
            audio = base64.standard_b64encode(file.read()).decode()
            final_audio = f"{audio}"
        return final_audio
