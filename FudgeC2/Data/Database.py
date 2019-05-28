# SQL Alchemy stuffs
from sqlalchemy import create_engine, func, extract
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from Data.models import Users, ResponseLogs, Implants, ImplantLogs, Campaigns, CampaignUsers, GeneratedImplants, AppLogs, CampaignLogs,declarative_base
from Storage.settings import Settings
import uuid
import bcrypt
import time
import ast
import random
from Data.Logging import Logging
from Data.CampaignLogging import *
L = Logging()
CL = CampaignLoggingDecorator()
class Database():
    def __init__(self):

        engine = create_engine("sqlite:///Storage/{}?check_same_thread=False".format(Settings.database_name))
        # -- TODO: RefactorGet_AllCampaignImplants
        self.selectors = {
            "uid": Users.uid,
            "email": Users.user_email
        }
        self.Session = scoped_session(sessionmaker(bind=engine, autocommit=False))
        """:type: sqlalchemy.orm.Session""" # PyCharm type fix. Not required for execution.

        self.__does_admin_exist()

        #self.

    # CL = ""
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.Session.remove()

    def raw_query(self, sql_query_string, sqlinput=None):
        return []

    ## -- Queries from here on -- #
    def test(self, email):
        query = self.Session.query(Users).filter(Users.user_email == email)
        for x in query:
            print("-",x.password)
        # rows = self.Session.query(Users).filter(extract('day', Account.created_at) == int(now.day),extract('month', Account.created_at) == now.month).all()
        return query
    def JoinTest(self,user):
        # --
        q=self.Session.query(Campaigns.title,Users.user_email,CampaignUsers.permissions).filter(Users.user_email==user,CampaignUsers.uid==Users.uid).group_by(Campaigns.title).all()
        #q = self.Session.query(Campaigns,CampaignUsers).join(CampaignUsers)
        for x in q:
            print(x)


    ## -- PRIVATE METHODS -- #

    def __get_userid__(self,email):
        # -- Require further improvement i.e try:catch
        query = self.Session.query(Users.uid).filter(Users.user_email == email).first()
        if query == None:
            return False
        else:
            return query[0]
        # TODO: Improve and avoid race conditions.
    def __update_last_logged_in__(self,email):
        Result = self.Session.query(Users).filter(Users.user_email == email).update({"last_login": (time.time())})
        self.Session.commit()
        return True
    def __get_campaignid__(self,campaign):
        #TODO: Improve the Try/Catch
        q = self.Session.query(Campaigns.cid).filter(Campaigns.title==campaign).one()
        if q == None:
            return False
        else:
            print(q[0])
    def __splice_implants_and_generated_implants__(self, obj):
        # Hand a list of genrerated imaplnts and implabt list pairs and splice them togerther returning in a [{},{}] format
        CompletedList = []
        if type(obj) == list:
            for x in obj:
                ResultofSplice={}
                if str(type(x)) == "<class 'sqlalchemy.util._collections.result'>":
                    ResultofSplice = {**x[0].__dict__, **x[1].__dict__}
                CompletedList.append(ResultofSplice)
            return CompletedList
        else:
            ResultofSplice = {}
            if str(type(obj)) == "<class 'sqlalchemy.util._collections.result'>":
                ResultofSplice = {**obj[0].__dict__, **obj[1].__dict__}
            CompletedList.append(ResultofSplice)
        return CompletedList

    def __hash_cleartext_password__(self,password):
        # Hashed a clear text password ready for insertion into the database
        password_bytes = password.encode()
        hashedpassword = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        if bcrypt.checkpw(password_bytes, hashedpassword):
            return hashedpassword
        else:
            return False

    def __does_admin_exist(self):
        # -- Checking for admin existance, for first-time launches.
        if  not self.__get_userid__("admin"):
            print("Creating first-time admin account.")
            if not self.Add_User("admin", "letmein", True):
                raise ValueError("Error creating admin account in empty database.")

    # --
    # -- PUBLIC METHODS -- #
    # --
    def Add_User(self, Username, Password, Admin=False):
        # -- TODO: This needs a more rebust response Try/Except.
        query = self.Session.query(Users.password, Users.uid).filter(Users.user_email==Username).all()
        for x in query:
            return False
        users = Users(user_email=Username,password=self.__hash_cleartext_password__(Password),admin=Admin,last_login=time.time())
        self.Session.add(users)
        self.Session.commit()
        return True


    def User_HasCompletedFirstLogon(self,email):
        # -- Return (true/false)
        HasLoggedOn = self.Session.query(Users).filter(Users.first_logon == 0,Users.user_email == email).all()
        if HasLoggedOn:
            print(HasLoggedOn)
            return True
        else:
            print("Else: ",HasLoggedOn)
            return False
    def User_ChangePasswordOnFirstLogon(self,guid, current_password,new_password):
        UserObj = self.Session.query(Users).filter(Users.first_logon_guid==guid).first()
        if UserObj == None:
            return False
        else:
            if bcrypt.checkpw(current_password.encode(), UserObj.password):
                print("Correct PW")
                hashedpassword = self.__hash_cleartext_password__(new_password)
                Result = self.Session.query(Users).filter(Users.first_logon_guid==guid).update({"password":(hashedpassword),"first_logon":1})
                self.Session.commit()
                UpdatedUserObj = self.Session.query(Users).filter(Users.password==hashedpassword).first()
                print(dir(UpdatedUserObj))
                return UpdatedUserObj
            else:
                return False

    def Get_UserFirstLogonGuid(self, email):
        pre_guid =str(uuid.uuid4())
        Result = self.Session.query(Users).filter(Users.user_email == email).update({"first_logon_guid": (pre_guid)})
        self.Session.commit()
        return pre_guid


    def Create_Campaign(self, title, email, description="Default"):
        # check user:
        uid=self.__get_userid__(email)
        if uid == False:
            return False
        campaign = Campaigns(title=title,created=time.time(),description=description)
        #c_user = CampaignUsers(cid=,uid=,read=,write=)
        self.Session.add(campaign)
        try:
            self.Session.commit() # flush check if this will work...
            #q=self.Session.query(Campaigns.cid).filter(Campaigns.title==title).one()
            #print("1",q[0])
            if self.Add_CampaignUser(title,email,2):
                print("Success adding a new campaign user.")
                return True
        except Exception as e:
            print(e)
            return False

        # Make campaign (check no dup name)
        # Add user to campaign users
        # commit or rollback.
    def Add_CampaignUser(self,CampaignTitle,Email,Permission=1):
        # a
        cid = self.Session.query(Campaigns.cid).filter(Campaigns.title==CampaignTitle).one()[0]
        uid = self.Session.query(Users.uid).filter(Users.user_email==Email).one()[0]
        print(cid,uid)
        query=CampaignUsers(cid=cid,uid=uid,permissions=Permission)
        try:
            self.Session.add(query)
            self.Session.commit()
            return True
        except Exception as e:
            print("Func:Add_CampaignUser:",e)
            return False

    def Get_CampaignInfo(self,campaign,email):
        # -- Not used?
        q = self.Session.query(Campaigns).filter(Campaigns.title==campaign,Users.user_email==email).all()
        for x in q:
            print("User:",email,x.title,x.description,x.created)

    def Get_AllUserCampaigns(self,email):
        q=self.Session.query(Campaigns.cid, Campaigns.title).filter(
            Users.user_email==email,
            CampaignUsers.uid==Users.uid,
            Campaigns.cid==CampaignUsers.cid
        ).group_by(Campaigns.title).all()
        campaignList = []
        campDict = {}
        for x in q:
            campDict[x[0]]=x[1]
            #print(x)
            campaignList.append(x[0])
        return campDict
    def Get_AllImplantIDFromTitle(self, Implant_title):
        # -- Return list containing generated implant dictionaries.
        IID = self.Session.query(GeneratedImplants, Implants).filter(Implants.iid == GeneratedImplants.iid, GeneratedImplants.generated_title == Implant_title).all()
        IID = self.__splice_implants_and_generated_implants__(IID)
        return IID

    # -- Implant Content --#
    def Add_Implant(self, cid, title, url, port, beacon, initial_delay, comms_http=0, comms_https=0, comms_dns=0, comms_binary=0, description="Implant: Blank description.", obfuscation_level=0):
        # -- TODO: Refactor
        print("In Add_Implant_Function")
        implant = Implants(cid=cid,title=title)
        stager_key= random.randint(10000,99999)
        NewImplant = Implants(cid=cid,title=title,description=description,callback_url=url,stager_key=stager_key,file_hash="0",filename="0",
                              port=port,
                              beacon=beacon,
                              initial_delay=initial_delay,
                              comms_http=comms_http,
                              comms_https=comms_https,
                              comms_dns=comms_dns,
                              comms_binary = comms_binary,
                              obfuscation_level = obfuscation_level
                              )
        self.Session.add(NewImplant)
        try:
            self.Session.commit()
            q=self.Session.query(Implants).first()
            print(q)
            return True
        except Exception as e:
            print("db.Add_Implant: ",e)
            return e


    # -- LOGIN CONTENT --#
    @L.log("User logged in.")
    def Get_UserObjectLogin(self, email, password):
        # Auths a user and returns user object
        print(email,password)
        user = self.Session.query(Users).filter(Users.user_email==email).first()
        if user != None:
            #print(password.encode(), user.password.encode())
            a = user.password
            if bcrypt.checkpw(password.encode(), a):
                self.__update_last_logged_in__(email)
                return user
            else:
                return False
        else:
            return False

    def Get_CampaignNameFromCID(self,cid):
        # -- Clean up --#
        name=self.Session.query(Campaigns.title).filter(Campaigns.cid==cid).first()
        if name == None:
            return "Unknown"
        return name.title

    def Get_UserObject(self, email):
        # Auths a user and returns user object:
        user = self.Session.query(Users).filter(Users.user_email==email).first()
        #user = Users.query.filter_by(user_email==email).first()
        #print(user.password)
        return user
    def Get_AllCampaignImplants(self, cid):
         # THIS IS THE OLD IMPLANT!
        # implant= self.Session.query(Implants.iid, Implants.title, Implants.description, Implants.callback_url, Implants.stager_key).filter(Implants.cid==cid).all()
        a = []
        implant = self.Session.query(GeneratedImplants, Implants).filter(GeneratedImplants.iid==Implants.iid, Implants.cid == cid).all()
        if implant ==None:
            print("Campaign has no implants.")
        results = self.__splice_implants_and_generated_implants__(implant)
        return results

    def Get_AllImplantBaseFromCid(self,cid):
        # -- THIS NEED TO BE REBUILT
        SA_Implants = self.Session.query(Implants).filter(Implants.cid == cid).all()
        processed_implants = []
        for implant in SA_Implants:
            b= implant.__dict__
            if '_sa_instance_state' in b:
                del b['_sa_instance_state']
            processed_implants.append(b)

        if processed_implants != None:
            return processed_implants
        else:
            return []

    def Get_AllGeneratedImplantsFromCID(self, CID):
        raw_implants= self.Session.query(GeneratedImplants, Implants).filter(GeneratedImplants.iid == Implants.iid, Implants.cid == CID).all()
        generated_implants = self.__splice_implants_and_generated_implants__(raw_implants)
        if generated_implants != None:
            return generated_implants
        else:
            return False

    def Get_GeneratedImplantDataFromUIK(self,UIK):
        # -- Pulls all configuration data for a generated implant based on UIK.
        # --    Used when implants checkin.
        a = self.Session.query(GeneratedImplants, Implants).filter(Implants.iid==GeneratedImplants.iid, GeneratedImplants.unique_implant_id == UIK).all()
        a = self.__splice_implants_and_generated_implants__(a)
        if a != None:
            return a
        else:
            return False

    def Convert_UniqueImplantKey(self, IID):
        print("TODO")
        # -- Check for reference and remove after.

    @CL.log_implant_activation
    def Register_NewImplantFromStagerKey(self, StagerKey):
        # -- We are registering a NEW implant and generating a unique_stager_key (or UIK)
        # -- Moving forward all reference to ImplantKey/UII should be changed to StagerID

        I = self.Session.query(Implants).filter(Implants.stager_key==StagerKey).first()
        if I != None:
            UIK = random.randint(000000,999999)
            new_title = str(I.title) +"_"+ str(UIK)
            GI=GeneratedImplants(unique_implant_id = UIK,last_check_in = 0,current_beacon = I.beacon,iid = I.iid, generated_title = new_title, time=int(time.time()))
            self.Session.add(GI)
            try:
                self.Session.commit()
                q = self.Session.query(GeneratedImplants).first()
                print("~",q)

            except Exception as e:
                print("db.Add_Implant: ", e)
                return False

            GetImplant = self.Session.query(GeneratedImplants, Implants).filter(Implants.iid == GeneratedImplants.iid, GeneratedImplants.unique_implant_id == UIK).first()
            GetImplant = self.__splice_implants_and_generated_implants__(GetImplant)
            # GetImplant=self.Session.query(Implants,GeneratedImplants).filter(GeneratedImplants.iid == Implants.iid).filter(Implants.stager_key == StagerKey).first()
            print("Post splicechecl: ",GetImplant)
            # -- Return Raw objects, and caller to manage them,
            return GetImplant
        return False


    # -- Active Implant Queries -- #
    # ---------------------------- #
    def Update_ImplantLastCheckIn(self, GeneratedImplantKey):
        # -- TODO: Create error handling around invalid GeneratedImplantKey
        a =self.Session.query(GeneratedImplants).filter(GeneratedImplants.unique_implant_id==GeneratedImplantKey).update({"last_check_in": (int(time.time()))})
        self.Session.commit()

    @CL.log_cmdreg
    def Register_ImplantCommand(self, username, uik, command,  cid=0):
        # -- Requirements: username unique_implant_key, command
        # -- Checks: User can register commands against a generated implant

        uid = self.__get_userid__(username)

        result = self.Session.query(CampaignUsers,
                                    Implants,
                                    GeneratedImplants
                                    ).filter(
                            CampaignUsers.uid == uid,
                            Campaigns.cid == CampaignUsers.cid,
                            Implants.cid == Campaigns.cid,
                            Implants.iid ==GeneratedImplants.iid,
                            GeneratedImplants.unique_implant_id == uik).all()

        if len(result) == 0:
            print("No Implant <--> User association")
            return False
        for line in result:
            if line[0].permissions == 2:
                # uid
                cid=line[0].cid
                new_implant_log=ImplantLogs(cid=cid,uid=uid,time=time.time(),log_entry=command,uik=uik,read_by_implant=0)
                self.Session.add(new_implant_log)
                try:
                    self.Session.commit()
                    q = self.Session.query(ImplantLogs).first()
                    #print(q)
                    return True
                except Exception as e:
                    print("db.Register_ImplantCommand: ", e)
                    return False
            else:
                # -- Incase non 0/1 response --#
                return False
    def Get_RegisteredImplantCommandsFromUIK(self, UIK):
        # -- Return List
        Logs = self.Session.query(ImplantLogs).filter(ImplantLogs.uik == UIK).all()
        if Logs != None:
            return Logs
        else:
            return []

    def Get_RegisteredImplantCommandsFromCID(self, CID):
        Logs = self.Session.query(ImplantLogs).filter(ImplantLogs.cid == CID).all()
        if len(Logs) > 0:
            return Logs
        else:
            return []

    @CL.log_cmdpickup
    def Register_ImplantCommandPickup(self, record):
        ImplantPickup = self.Session.query(ImplantLogs).filter(
            ImplantLogs.uik == record.uik,
            ImplantLogs.log_entry == record.log_entry,
            ImplantLogs.time == record.time).update({'read_by_implant':(int(time.time()))})
        try:
            self.Session.commit()
            return True
        except Exception as E:
            print("Exception: ",E)
            return False

    @CL.log_cmdresponse
    def Register_ImplantResponse(self,cid,UIK,Response, c2_protocol):
        # -- TODO: REBUILD
        # Pull back the first record which matches the UIK, contain both the Campaign the IID is associated from the implant the UIk is associated with.
        info=self.Session.query(Implants,Campaigns,GeneratedImplants).filter(Campaigns.cid==Implants.cid
                                                           ).filter(Implants.iid==GeneratedImplants.iid).filter(GeneratedImplants.unique_implant_id==UIK).first()
        iid = info[0].iid
        cid = info[1].cid
        uik = info[2].unique_implant_id
        # print("Record\ncid:    {}\niid:    {}\nentry:  {}\ntime:   {}".format(cid,iid,Response,int(time.time())))
        RL=ResponseLogs(cid=cid, uik=uik, log_entry=Response,time=int(time.time()))
        self.Session.add(RL)
        try:
            print("Commiting values")
            self.Session.commit()
            return True
        except Exception as E:
            print(E)




    def Get_CampaignImplantResponses(self, cid):
        # -- TODO: Refactor
        a=self.Session.query(ResponseLogs).filter(ResponseLogs.cid == cid).all()
        ReturnList=[]
        for x in a:
            a = x.__dict__
            if '_sa_instance_state' in a:
                del a['_sa_instance_state']
            b = self.Session.query(GeneratedImplants.generated_title).filter(GeneratedImplants.unique_implant_id==a['uik']).first()
            if b != None:
                a['title']=b[0]
            ReturnList.append(a)
        return(ReturnList)

        # -- This may be a single or list: Check and convert to list implictly?


    # -- Campaign Settings Content -- #
    # ------------------------------- #
    def Get_SettingsUsers(self, cid, user):
        # TODO: Create a list of user dicts with name, uid, and read/write to be returned to a table with radio tabs.
        # TODO: Clean up
        User = self.Session.query(Users.user_email, Users.uid).group_by(Users.user_email)
        final=[]
        for x in User:
            tmp={"user":x[0],"uid":x[1]}
            entry = self.Session.query(CampaignUsers).filter(CampaignUsers.cid ==cid, CampaignUsers.uid== x[1]).first()
            # print("::")
            if entry != None:
                tmp['permissions'] = entry.permissions
            else:
                tmp['permissions'] = 0
            final.append(tmp)

        x = [ i for i in final if i['user'] != user]
        return x

    def User_SetCampaignAccessRights(self,user,cid, rights):
        '''
        :param user: Int
        :param cid: Int
        :param rights: Int [0/1/2]
        :return: bool
        '''
        print(user,cid, rights)
        a = self.Session.query(CampaignUsers).filter(CampaignUsers.uid == user, CampaignUsers.cid == cid).first()
        if a == None:
            PermissionUpdate = CampaignUsers(cid=cid,uid=user,permissions=rights)
            self.Session.add(PermissionUpdate)
            try:
                self.Session.commit()
                return True
            except Exception as E:
                print(E)
                return False
        else:
            Result = self.Session.query(CampaignUsers).filter(CampaignUsers.cid==cid, CampaignUsers.uid==user).update({'cid':cid,'uid':user,'permissions':rights})
            self.Session.commit()
        return

    # -- Access Control Checks
    def Verify_UserCanAccessCampaign(self,Users,CID):
        # -- TODO: Reduce line count, and if,elif, and else statment to a cleaner alternative.
        User = self.__get_userid__(Users)
        if User == None:
            return False
        R = self.Session.query(CampaignUsers).filter(CampaignUsers.cid==CID, CampaignUsers.uid==User).first()
        if R == None or R.permissions <=0:
            return False
        elif R.permissions >=1:
            return True

    def Verify_UserCanWriteCampaign(self, username,cid):
        # Return bool
        uid = self.__get_userid__(username)
        if uid == None:
            return False
        R = self.Session.query(CampaignUsers).filter(CampaignUsers.cid == cid, CampaignUsers.uid == uid).first()
        if R == None or R.permissions < 2:
            return False
        elif R.permissions >= 2:
            return True
    def Verify_UserCanReadCampaign(self, username, cid):
        uid = self.__get_userid__(username)
        if uid == None:
            return False
        R = self.Session.query(CampaignUsers).filter(CampaignUsers.cid == cid, CampaignUsers.uid == uid).first()
        if R == None or R.permissions < 1:
            return False
        elif R.permissions >= 1:
            return True


    # -- App Logging Classes -- #
    # ------------------------- #
    def Log_ApplicationLogging(self, values):
        campaign = AppLogs(type=values['type'], data=values['data'])
        self.Session.add(campaign)
        try:
            self.Session.commit()  # flush check if this will work...
        except:
            return False

    def Log_CampaignAction(self,dict_of_stuff):
        try:
            logs = CampaignLogs(
                user=dict_of_stuff['user'],
                campaign=dict_of_stuff['campaign'],
                time=dict_of_stuff['time'],
                log_type=dict_of_stuff['log_type'],
                entry=str(dict_of_stuff['entry'])
            )
            self.Session.add(logs)
            self.Session.commit()
            print("Log: Log_CampaignAction::"+dict_of_stuff['log_type']+" success.")
            return True
        except Exception as e:
            print(e)
            return False

    def Log_GetCampaignActions(self,cid):
        R = self.Session.query(CampaignLogs).filter(CampaignLogs.campaign == cid).all()
        ret_dict = {}

        for count, row in enumerate(R):
            ret_dict[count]=row.__dict__
            del ret_dict[count]['_sa_instance_state']
            ret_dict[count]['entry'] = ast.literal_eval(ret_dict[count]['entry'])
        return ret_dict
