from Database import Database
class UserManagementController():
    db = Database()
    # def __init__(self, DatabaseConnector):
    #     print(type(DatabaseConnector))
    #     if str(type(DatabaseConnector)) == "<class 'Database.Database'>":
    #         self.db = DatabaseConnector
    #         return
    #     else:
    #         raise ValueError("Not a valid container")

    def AddUser(self, formdata, submitting_user):
        print("Form: ",formdata,"\nUser: ",submitting_user)
        U = self.db.Get_UserObject(submitting_user)
        print(U.admin)
        if U.admin:
            print("Admin")
            # -- Validate
