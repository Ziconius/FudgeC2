import time
from Data.models import Users, ImplantTemplate, Campaigns, CampaignUsers, GeneratedImplants
from Data.CampaignLogging import CampaignLoggingDecorator

CL = CampaignLoggingDecorator()


class DatabaseCampaign:

    def __init__(self, source_database, session):
        # TODO: Check sesion type
        self.Session = session
        self.db_methods = source_database

    @CL.campaign_add_user
    def Add_CampaignUser(self, campaign_title, email, permission=1):
        cid = self.Session.query(Campaigns.cid).filter(Campaigns.title == campaign_title).one()[0]
        uid = self.Session.query(Users.uid).filter(Users.user_email == email).one()[0]
        query = CampaignUsers(cid=cid, uid=uid, permissions=permission)
        try:
            self.Session.add(query)
            self.Session.commit()
            return True
        except Exception as e:
            print("Func:Add_CampaignUser:", e)
            return False

        # TODO: Create logging
    def create_campaign(self, user, title, description="Default"):
        campaign = Campaigns(title=title, created=time.time(), description=description)
        self.Session.add(campaign)
        try:
            self.Session.commit()
            if self.Add_CampaignUser(title, user, 2):
                print("Success adding a new campaign user.")
                return True
        except Exception as e:
            print(e)
            return False

    def get_all_user_campaigns(self, email):
        campaigns_by_title = self.Session.query(Campaigns.cid, Campaigns.title).filter(
            Users.user_email == email,
            CampaignUsers.uid == Users.uid,
            Campaigns.cid == CampaignUsers.cid
            ).group_by(Campaigns.title).all()

        campaign_dict = {}
        for campaign in campaigns_by_title:
            campaign_dict[campaign[0]] = campaign[1]

        return campaign_dict

    def Get_CampaignNameFromCID(self, cid):
        # -- Clean up --#
        name = self.Session.query(Campaigns.title).filter(Campaigns.cid == cid).first()
        if name is None:
            return "Unknown"
        return name.title

    def get_campaign_user_settings(self, cid):
        # Returns list containing any number of dictionary elements containing the configuration of the users
        #   in relation to the submitted campaign. Omits the the user which submits the
        user_list = self.Session.query(Users.user_email, Users.uid).group_by(Users.user_email)
        final = []
        for x in user_list:
            tmp = {"user": x[0], "uid": x[1]}
            entry = self.Session.query(CampaignUsers).filter(CampaignUsers.cid == cid, CampaignUsers.uid == x[1]).first()
            if entry is not None:
                tmp['permissions'] = entry.permissions
            else:
                tmp['permissions'] = 0
            final.append(tmp)
        return final

    # TODO: Add logging
    @CL.campaign_modify_user_rights
    def User_SetCampaignAccessRights(self, username, user_id, cid, rights):
        # :param user: Int
        # :param cid: Int
        # :param rights: Int [0/1/2]
        # :return: bool
        a = self.Session.query(CampaignUsers).filter(CampaignUsers.uid == user_id, CampaignUsers.cid == cid).first()
        if a is None:
            permission_update = CampaignUsers(cid=cid, uid=user_id, permissions=rights)
            self.Session.add(permission_update)
            try:
                self.Session.commit()
                return True
            except Exception as E:
                print(E)
                return False
        else:
            self.Session.query(CampaignUsers).filter(
                CampaignUsers.cid == cid,
                CampaignUsers.uid == user_id).update({'cid': cid, 'uid': user_id, 'permissions': rights})
            self.Session.commit()
        return True

    def Verify_UserCanAccessCampaign(self, users, cid):
        # -- TODO: Reduce line count, and if,elif, and else statment to a cleaner alternative.
        user = self.db_methods.__get_userid__(users)
        if user is None:
            return False
        campaign_user = self.Session.query(CampaignUsers).filter(CampaignUsers.cid == cid,
                                                                 CampaignUsers.uid == user).first()

        if campaign_user is None or campaign_user.permissions <= 0:
            return False
        elif campaign_user.permissions >= 1:
            return True

    def Verify_UserCanWriteCampaign(self, username, cid):
        # Return bool
        uid = self.db_methods.__get_userid__(username)
        if uid is None:
            return False
        campaign_user = self.Session.query(CampaignUsers).filter(CampaignUsers.cid == cid,
                                                                 CampaignUsers.uid == uid).first()

        if campaign_user is None or campaign_user.permissions < 2:
            return False
        elif campaign_user.permissions >= 2:
            return True

    def Verify_UserCanReadCampaign(self, username, cid):
        # Returns a boolean
        uid = self.db_methods.__get_userid__(username)
        if uid is None:
            return False
        campaign_user = self.Session.query(CampaignUsers).filter(CampaignUsers.cid == cid,
                                                                 CampaignUsers.uid == uid).first()

        if campaign_user is None or campaign_user.permissions < 1:
            return False
        elif campaign_user.permissions >= 1:
            return True

    def get_all_campaign_implant_templates_from_cid(self, cid):
        implant = self.Session.query(GeneratedImplants, ImplantTemplate).filter(GeneratedImplants.iid == ImplantTemplate.iid,
                                                                         ImplantTemplate.cid == cid).all()
        if implant is None:
            return False
        results = self.db_methods.__splice_implants_and_generated_implants__(implant)
        return results
