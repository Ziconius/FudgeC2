import requests
from distutils.version import LooseVersion

from Data.Database import Database
from Storage.settings import Settings


class AppManager:
    db = None

    def __init__(self):
        self.db = Database()

    @staticmethod
    def check_software_version():
        # Returns "True" if the software is behind Git Hubs master version file.
        url = "https://raw.githubusercontent.com/Ziconius/FudgeC2/master/FudgeC2/Storage/version.txt"
        try:
            request_result = requests.get(url, timeout=1)
            master = request_result.content.decode()
            if LooseVersion(master) > LooseVersion(Settings.version):
                return True
            else:
                return False
        except Exception as exception_text:
            print("check_software_version(): ",exception_text)
            return False

    @staticmethod
    def get_software_verision_number():
        try:
            version = Settings.version
            return version
        except Exception as exception_text:
            print(exception_text)
            return "0.0.0"

    @staticmethod
    def get_software_verision_name():
        try:
            version = Settings.version_name
            return version
        except Exception as exception_text:
            print(exception_text)
            return "Unknown"

    def campaign_create_campaign(self, user, form):
        # Responsible for validating admin account, and campaign title exists.
        if self.db.user.User_IsUserAdminAccount(user) is True:
            if 'title' in form and 'description' in form:
                if form['title'].strip() != "":
                    if self.db.campaign.create_campaign(user, form['title'].strip(), form['description'].strip()) is True:
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
        return self.db.campaign.Get_CampaignNameFromCID(cid)

    # TODO: Implement returning app logs to web app.
    def get_application_logs(self, username):
        # is user admin if not return false.
        if self.db.user.User_IsUserAdminAccount(username):
            return self.db.get_application_logs()
        else:
            return []
