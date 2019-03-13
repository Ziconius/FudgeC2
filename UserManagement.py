from Database import Database
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
                Result_Dict['reason']=str(formdata['UserName']+" now created. Password is: "+pw)
            else:
                Result_Dict['result'] = False
                Result_Dict['reason'] = "User already exists."
            print("Admin")
            # -- Validate

        return Result_Dict

    def AddUserToCampaign(self, Submitter, User, Campaign, Rights=0):
        print("Here")
        print(Submitter)
        S = self.db.Get_UserObject(Submitter)
        if S.admin:
            U = self.db.Get_UserObject(User)
            if U:
                C = self.db.Get_CampaignInfo(Campaign,Submitter)
                if C:
                    self.db.User_SetCampaignAccessRights(U.uid, C.cid,Rights)
        else:
            return False