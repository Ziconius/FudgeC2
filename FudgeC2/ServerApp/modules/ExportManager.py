import os
import time
import base64
import random
import string

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from sqlalchemy import Column, String, text, create_engine, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from Data.Database import Database

Base = declarative_base()
metadata = Base.metadata



class ExportedCampaign(Base):
    __tablename__ = 'export_data'
    uid = Column(INTEGER, primary_key=True)
    user = Column(String(255), nullable=False)
    time = Column(String(255), nullable=False)
    log_type = Column(String(255), nullable=False)
    entry = Column(String(255), nullable=False)


class DbCreator:
    filename = ""
    Session = None

    def __init__(self, filename):
        filename = filename

        path = os.getcwd() + "/Storage/ExportedCampaigns/"
        database_name = filename

        engine = create_engine(f"sqlite:///{path}/{database_name}?check_same_thread=False", echo=False)
        Base.metadata.create_all(engine)
        self.Session = scoped_session(sessionmaker(bind=engine, autocommit=False))
        """:type: sqlalchemy.orm.Session"""  # PyCharm type fix. Not required for execution.


# Shell for exporting a campaign for FudgeC2 Viewer application.
class CampaignExportManager:
    export_db = None
    db = Database()
    file_dir = "Storage/ExportedCampaigns/"

    def test(self, filename, file_dir):
        # check file name for uniqueness.
        self.export_db = DbCreator(filename)
        a = self.export_db.Session.query(ExportedCampaign).all()
        return a

    def test_put(self, a, b, c, d):
        logs = ExportedCampaign(
            user=str(a),
            time=str(b),
            log_type=str(c),
            entry=str(d)
        )
        self.export_db.Session.add(logs)
        self.export_db.Session.commit()

    def _validate_user_(self, username, cid):
        if self.db.user.User_IsUserAdminAccount(username) is not False:
            if self.db.campaign.Verify_UserCanReadCampaign(username, cid) is not False:
                return True
        return False

    def get_encrypted_file(self, username, cid, filename):
        if self._validate_user_(username, cid) is False:
            return False

        a = os.listdir(self.file_dir)
        if filename in a:
            return filename
        else:
            return False

    def export_campaign_database(self, username, cid):
        if self._validate_user_(username, cid) is False:
            return False

        db = self._generate_database_(cid)
        if db is False:
            return False

        # db contains(filename, file_path, password)
        result = self.encrypt_file(db[0], db[1], db[2])
        if result is False:
            return
        return result[0], result[1]

    def _generate_database_(self, cid):
        # DONE  get information (func)
        # check database export directory exists
        # DONE check file doesn't exist
        # DONE create campaign_name_unixtime
        # DONE create database
        # DONE encrypt
        # DONE return file, return password

        password = str(''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=12)))
        raw_logs = self.db.Log_GetCampaignActions(cid)

        campaign_name = self.db.campaign.Get_CampaignNameFromCID(cid)
        file_name = "{}_{}".format(campaign_name.replace(" ", "_"), int(time.time()))
        file_dir = "Storage/ExportedCampaigns/"
        a = os.listdir(file_dir)
        database = file_dir + file_name
        if file_name in a:
            return False

        b = self.test(file_name, file_dir)
        for x in raw_logs:
            self.test_put(raw_logs[x]['user'], raw_logs[x]['time'], raw_logs[x]['log_type'], raw_logs[x]['entry'])

        return file_name, file_dir, password

    def get_information(self):
        return

    def database_file_storage_check(self):
        return

    def encrypt_file(self, filename, file_path, password):

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
        # key = b''  # Use one of the methods to get a key (it must be the same when decrypting)
        input_file = file_path+filename
        output_file = file_path+filename+".encrypted"

        with open(input_file, 'rb') as f:

            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(output_file, 'wb') as f:
            f.write(encrypted)

        return filename+".encrypted", password
