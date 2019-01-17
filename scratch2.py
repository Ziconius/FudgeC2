from Database import Database

db = Database()

#db.__get_userid__("admin")
#db.Add_User("AAdministrator","Password123", True)
#db.__get_campaignid__("Boots Ltd.")
#print("[Database]::",db.Create_Campaign("Context2_IS2", "admin_3","This is a non-default description!"))
#db.JoinTest("admin")
#db.Get_CampaignInfo("Boots Ltd.","admin")
#a = db.Get_AllUserCampaigns("admin")
print(db.Get_UserObjectLogin("admin","password"))