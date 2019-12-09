import secrets

from FudgeC2.Storage.settings import Settings

class DownloadFile:
    type = "FD"
    args = "base64 target file"
    input = "download_file"

    def process_implant_response(self, data, filepath):
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

    def implant_text(self):
        var = '''
# Download files from client - Not yet implemented
function {{ ron.obf_download_file }} ($b) {
    Write-Host "Downloading file: $b"
}'''
        return var
