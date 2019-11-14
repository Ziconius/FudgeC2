# This module is responsible for the post processing of all implant response information.
# It will extract, process, and store data based on which builtin functionality was used.
#   The class will be static with few public methods, and instead will focus on
import ast

from Data.Database import Database

class ImplantResponseProcessor:
    db = Database()

    def _system_info(self, data):
        # Username: Kris
        # Hostname: DESKTOP - SUMPM3F
        # Domain: WORKGROUP
        # Local IP: 192.168.2.130
        return None

    def process_command_response(self, command_id, command_response):
        a = self.db.implant.get_registered_implant_commands_by_command_id(command_id)
        b = ast.literal_eval(a['log_entry'])

        return command_response, None