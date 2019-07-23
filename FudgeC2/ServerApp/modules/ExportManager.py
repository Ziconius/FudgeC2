import os
import time
from Data.Database import Database


from sqlalchemy import Column, ForeignKey, String, text, create_engine
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
metadata = Base.metadata

class ExportedCampaign(Base):
    __tablename__ = 'export_data'
    uid = Column(INTEGER, primary_key=True)
    user = Column(String(255), nullable=False)
    time = Column(String(255), nullable=False)
    log_type = Column(String(255), nullable=False)
    entry = Column(String(255), nullable=False)
    # user_email = Column(String(255), nullable=False)
    # password = Column(String(255), nullable=False)
    # last_login = Column(String(255), nullable=False)
    # authenticated = Column(String, server_default=text("False"))
    # admin = Column(String(255), nullable=False)
    # first_logon = Column(INTEGER(1), nullable=False, default=0)
    # first_logon_guid = Column(String(32), nullable=False, default="0")


class DbCreator:
    filename = ""
    Session = None
    def __init__(self, filename):
        filename = filename
        print ("creating target file needs to be in init")

        metadata = Base.metadata

        path = os.getcwd() + "/Storage/ExportedCampaigns/"
        database_name = filename

        engine = create_engine("sqlite:///{}/{}?check_same_thread=False".format(path, database_name), echo=False)
        Base.metadata.create_all(engine)
        self.Session = scoped_session(sessionmaker(bind=engine, autocommit=False))
        """:type: sqlalchemy.orm.Session"""  # PyCharm type fix. Not required for execution.


# TODO: Create a auth log table.



# Shell for exporting a campaign for FudgeC2 Viewer application.
class CampaignExportManager:
    export_db = None
    db = Database()

    def test(self, filename, file_dir):
        # check file name for uniqueness.
        self.export_db = DbCreator(filename)
        a =self.export_db.Session.query(ExportedCampaign).all()
        print(a.__repr__())
        return a

    def test_put(self,a,b,c,d):
        logs = ExportedCampaign(
            user=str(a),
            time=str(b),
            log_type=str(c),
            entry=str(d)
        )
        self.export_db.Session.add(logs)
        self.export_db.Session.commit()

    def export_campaign_database(self, username, cid):
        # check user is admin
        if self.db.user.User_IsUserAdminAccount(username) is False:
            return False
        # check campaign exists
        if self.db.campaign.Verify_UserCanReadCampaign(username, cid) is False:
            return False
        # check user has read access to campaign
        db = self._generate_database_(cid)
        if db is False:
            return False

        # db contains(filename, file_path, password)
        self.encrypt_file(db[0],db[1],db[2])
        return "blah.sql", "encryption_password"

    def _generate_database_(self, cid):
        # DONE  get information (func)
        # check database export directory exists
        # DONE check file doesn't exist
        # DONE create campaign_name_unixtime
        # create database
        # encrypt
        # return file, return password
        password = "blahBlahBLAH!"
        raw_logs = self.db.Log_GetCampaignActions(cid)

        campaign_name = self.db.campaign.Get_CampaignNameFromCID(cid)
        file_name = "{}_{}".format(campaign_name.replace(" ","_"),int(time.time()))
        file_dir = "Storage/ExportedCampaigns/"
        a = os.listdir(file_dir)
        database = file_dir + file_name
        if file_name in a:
            return False
        print(database)

        b = self.test(file_name, file_dir)
        for x in raw_logs:
            print(raw_logs[x])
            self.test_put(raw_logs[x]['user'],raw_logs[x]['time'],raw_logs[x]['log_type'],raw_logs[x]['entry'])



        return file_name, file_dir, password

    def get_information(self):
        return

    def database_file_storage_check(self):
        return

    def encrypt_file(self, filename, file_path, password):

        import base64
        import os
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

        password_provided = password  # This is input in the form of a string
        password = password_provided.encode()  # Convert to type bytes
        salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))


        from cryptography.fernet import Fernet
        #key = b''  # Use one of the methods to get a key (it must be the same when decrypting)
        input_file = file_path+filename
        output_file = file_path+filename+".encrypted"

        with open(input_file, 'rb') as f:

            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(output_file, 'wb') as f:
            f.write(encrypted)

