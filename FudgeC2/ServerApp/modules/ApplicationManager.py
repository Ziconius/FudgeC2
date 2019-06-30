import requests
from distutils.version import LooseVersion
from FudgeC2.Data.Database import Database


class AppManager:
    db = None

    def __init__(self):
        self.db = Database()

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
                    return True
                else:
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

    def campaign_create_campaign(self, user, form):
        # Responsible for validating admin account, and campaign title exists.
        if self.db.User_IsUserAdminAccount(user) is True:
            if 'title' in form and 'description' in form:
                if form['title'].strip() != "":
                    if self.db.create_campaign(user, form['title'].strip(), form['description'].strip()) is True:
                        return True, "Campaign created successfully."
                    else:
                        return False, "Unknown error."
                else:
                    return False, "You must supply both title and description values."
            else:
                return False, "You must supply both title and description values."
        else:
            return False, "You do not have admin permissions to create a campaign."

    def campaign_get_campaign_name_from_cid(self, cid):
        return self.db.Get_CampaignNameFromCID(cid)