import random
import string

from Data.Database import Database

class UserManagementController:
    db = Database()
    def add_new_user(self, formdata=None, submitting_user=None):
        # -- Refacteror/Clean Add failure checks
        # -- Check for the keys in formdata, if none then return an error.
        # -- UserName/is_admin

        Result_Dict = {
            "action":"Add New User",
            "result":None,
            "reason":None }
        # TODO: Review if minimum lenght usernames should be permitted.
        if len(formdata['UserName']) < 3:
            Result_Dict['result'] = False
            Result_Dict['reason'] = "Username too short"
            return Result_Dict
        U = self.db.user.Get_UserObject(submitting_user)
        print(U.admin)
        if int(U.admin) == 1:
            G = self.db.user.Get_UserObject(formdata['UserName'])
            admin = False
            if 'is_admin' in formdata:
                admin = True
            if G == None:
                N=8
                pw=''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=N))
                self.db.user.add_new_user(formdata['UserName'],pw,admin)
                Result_Dict['result']=True
                Result_Dict['reason']=str(formdata['UserName']+" now created. Password is: "+pw+" <br> Take note of this, it will not be visable again.")
            else:
                Result_Dict['result'] = False
                Result_Dict['reason'] = "User already exists."
            # -- Validate
        else:
            print("Not Admin user")
        print(Result_Dict)
        return Result_Dict

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
            print("Result of password reset User_ChangePasswordOnFirstLogon: {}".format(user_object))
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


