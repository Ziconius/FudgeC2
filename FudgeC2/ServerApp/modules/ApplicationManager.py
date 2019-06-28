import requests
from distutils.version import LooseVersion


class AppManager:

    @staticmethod
    def check_software_version():
        # Returns "True" if the software is behind GitHubs master version file.
        url = "https://raw.githubusercontent.com/Ziconius/FudgeC2/master/version.txt"
        try:
            request_result = requests.get(url, timeout=0.5)
            master = request_result.content.decode()
            with open("../version.txt", 'r') as v_file:
                local_version_number = str(v_file.read())
                if LooseVersion(master) > LooseVersion(local_version_number):
                    # print("Behind Master")
                    return True
                else:
                    # print("Not behind master")
                    return False
        except Exception as exception_text:
            print(exception_text)
            return False

    @staticmethod
    def get_software_verision_number():
        try:
            with open("../version.txt", 'r') as v_file:
                local_version_number = str(v_file.read())
                return local_version_number
        except Exception as exception_text:
            print(exception_text)
            return "0.0.0"