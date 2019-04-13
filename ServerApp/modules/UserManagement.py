from Data.Database import Database
import random
import string
class UserManagementController():
    db = Database()
    # def __init__(self, DatabaseConnector):
    #     print(type(DatabaseConnector))
    #     if str(type(DatabaseConnector)) == "<class 'Database.Database'>":
    #         self.db = DatabaseConnector
    #         return
    #     else:
    #         raise ValueError("Not a valid container")

    def AddUser(self, formdata=None, submitting_user=None):
        # -- Refacteror/Clean Add failure checks
        print("Form: ",formdata,"\nUser: ",submitting_user)
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
        U = self.db.Get_UserObject(submitting_user)
        print(U.admin)
        if U.admin:
            print("blah: ",formdata['UserName'])
            G = self.db.Get_UserObject(formdata['UserName'])
            admin = False
            if 'is_admin' in formdata:
                admin = True
            if G == None:
                N=8
                pw=''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
                print("::",pw)
                self.db.Add_User(formdata['UserName'],pw,admin)
                Result_Dict['result']=True
                Result_Dict['reason']=str(formdata['UserName']+" now created. Password is: "+pw+" <br> Take note of this, it will not be visable again.")
            else:
                Result_Dict['result'] = False
                Result_Dict['reason'] = "User already exists."
            print("Admin")
            # -- Validate

        return Result_Dict

    def AddUserToCampaign(self, Submitter, Users, Campaign, Rights=0):
        # -- Refactor with Try/Catch validating the Rights values.
        '''
        :param Submitter: string
        :param Users: Request.form (dict)
        :param Campaign: int
        :param Rights: int
        :return: bool
        '''
        # Remove Right kawgs.
        # Improve variable names
        # --
        if len(Users) < 1:
            print("too few")
            return False
        if Users:
            for User in Users:
                S = self.db.Get_UserObject(Submitter)
                if S.admin:
                    U = self.db.Get_UserObject(User)
                    if U:
                        C = self.db.Verify_UserCanAccessCampaign(S.user_email,Campaign)
                        if C:
                            self.db.User_SetCampaignAccessRights(U.uid, Campaign,Users[User])
                else:
                    return False
            return True