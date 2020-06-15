import random
import string

from email_client.email_notifications import EmailNotification
from Data.Database import Database

email_notification = EmailNotification()

class UserManagementController:
    db = Database()
    def process_new_user_account(self, formdata=None, submitting_user=None):
        # -- Refactor/Clean Add failure checks
        # -- Check for the keys in formdata, if none then return an error.
        # -- UserName/is_admin

        # Process - authorise user; Return False, "Insufficient permissions"
        # Parse input; Return False; "Input error"
        # Submit form; Return False; "Entry already exists"
        # Submit form; Check email; Send email; Return True; "User created, email notification"
        # Submit form; Check email; Send email; Return True; "User created, password is X"

        # Configuration vars
        generated_password_lenght = 12

        if self.db.user.User_IsUserAdminAccount(submitting_user) is not True:
            return False, "Insufficient permissions"

        name = formdata.get("name", None)
        username = formdata.get("username", None)
        user_email = formdata.get("user_email", None)
        # DEV: This will be refactored when granular permissions are implemented.
        admin = formdata.get("admin", False)
        password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits,
                                          k=generated_password_lenght))

        # Check if the input matches minimum:
        if len(username) < 3:
            return False, "Minimum username is 3 characters."

        # Assuming all checks passed, attempt to create the user in the database:
        state, msg = self.db.user.add_new_user(name, username, user_email, password, admin)
        if state is False:
            return False, msg
        else:
            if email_notification.email_notification_configuration():
                if email_notification.send_email_new_user_account(name, user_email, password):
                    return True, f"{username} account created. Login information has been emailed to: {user_email}"
                else:
                    return False, f"SMTP failed. New user account email notification failed. The temporary password for this account is: {password}<br>" \
                             f"Please take note of this as it will not be visible again."
            else:
                return True, f"{username} account created. The temporary password for this account is: {password}<br>" \
                             f"Please take note of this as it will not be visible again."

    def AddUserToCampaign(self, submitter, Users, Campaign, Rights=0):
        # -- Refactor with Try/Catch validating the Rights values.
        '''
        :param submitter: string
        :param Users: Request.form (dict)
        :param Campaign: int
        :param Rights: int
        :return: bool
        '''
        # Remove Right kawgs.
        # Improve variable names
        # --

        current_user_settings = self.db.campaign.get_campaign_user_settings(Campaign)

        if len(Users) < 1:
            return False
        S = self.db.user.Get_UserObject(submitter)
        if S.admin:
            for user in Users:
                for current_user in current_user_settings:
                    if user == current_user['user']:
                        if int(Users[user]) != int(current_user['permissions']):
                            self.db.campaign.User_SetCampaignAccessRights(user,
                                                                          current_user['uid'],
                                                                          Campaign,
                                                                          Users[user])
            return True
        else:
            return False

# -- New methods added in Tauren Herbalist to abstract functionality from the web application.
# --    This improves maintainability between frontend <-> Database changes.
    def user_login(self, user, password):
        # Returns False or user database object.
        return self.db.user.user_login(user, password)

    def get_first_logon_guid(self, user):
        return self.db.user.Get_UserFirstLogonGuid(user)

    def get_user_object(self, user):
        return self.db.user.Get_UserObject(user)

    def get_users_state(self, user):
        if self.db.user.User_IsUserAdminAccount(user):
            return self.db.user.get_user_state_list()
        return []
    def update_active_account_state(self, user, form):
        if self.db.user.User_IsUserAdminAccount(user):
            target_user = form['user']
            target_state = form['to_state']
            if self.db.user.change_account_active_state(target_user, target_state):
                return True
            return False
        else:
            return False
    def change_password_first_logon(self, form):
        pw_1 = form['password_one']
        pw_2 = form['password_two']
        pw_c = form['current_password']
        guid = form['id']
        if pw_1 == pw_2:
            user_object = self.db.user.User_ChangePasswordOnFirstLogon(guid, pw_c, pw_1)
            return user_object
        else:
            return False

    def get_current_campaign_users_settings_list(self, user, cid):
        # Returns a list of user dictionaries. Remove the current user so that a user cannot attempt to
        #   update, or remove their own configurations.
        list_of_user_settings = self.db.campaign.get_campaign_user_settings(cid)
        for x in list_of_user_settings:
            if x['user'] == user:
                list_of_user_settings.remove(x)
        return list_of_user_settings

    def campaign_get_user_access_right_cid(self, user, cid):
        # Return a boolean.
        return self.db.campaign.Verify_UserCanAccessCampaign(user, cid)

    def campaign_get_user_campaign_list(self, user):
        return self.db.campaign.get_all_user_campaigns(user)

    def campaign_get_all_implant_base_from_cid(self, user, cid):
        if self.db.campaign.Verify_UserCanReadCampaign(user, cid) is True:
            return self.db.campaign.get_all_campaign_implant_templates_from_cid(cid)
        return False


