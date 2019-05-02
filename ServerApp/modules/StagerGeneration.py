class StagerGeneration():
    db = None
    def __init__(self, db_pointer):
        self.db = db_pointer
    def GenerateStaticStagers(self,cid, user):
        ret_data = {}
        if self.db.Verify_UserCanAccessCampaign(user,cid):
            ImplantInfo = self.db.Get_AllImplantBaseFromCid(cid)
            if ImplantInfo != False:
                for implant in ImplantInfo:
                    ret_data[implant['name']]={"description":None,"url":None,"stager_string":None}
            return
        else:
            return
    def GenerateSingleStagerFile(self,cid,user,stager_type):
        if stager_type == "docx":
            return self.__generate_docx_stager_file()
        return

    def __generate_docx_stager_file(self):
        stager_file = "TempContent"
        return stager_file
