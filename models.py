# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Index, String, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, MEDIUMTEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

# TODO: Create a auth log table.

class Users(Base):
    __tablename__='users'
    uid =           Column(BIGINT(20), unique=True,primary_key=True)
    user_email =    Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    last_login = Column(String(255), nullable=False)
    authenticated = Column(String(), server_default=text("False"))
    admin = Column(String(255), nullable=False)
    first_logon = Column(INTEGER(1), nullable=False, default=0)
    first_logon_guid = Column(String(32), nullable=False, default=0)
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.user_email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class ResponseLogs(Base):
    __tablename__='response_logs'
    log_id = Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    cid = Column(INTEGER(11), nullable=False, index=True)
    uik = Column(INTEGER(11), nullable=False, index=True)
    log_entry = Column(String(255), nullable=False, unique=True)
    time = Column(INTEGER(11), nullable=False, index=True)

class Implants(Base):
    __tablename__='implants'
    iid=Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    stager_key = Column(String(255), nullable=False, unique=True)
    title = Column(String(255),nullable=False)
    cid = Column(INTEGER(11), nullable=False, index=True )
    file_hash=Column(String(255), nullable=True)
    filename=Column(String(255), nullable=True, unique=True)
    callback_url = Column(String(255), nullable=False, server_default=text("127.0.0.1"))
    port = Column(INTEGER(5), nullable=False, server_default=text("0"))
    description = Column(String(255))
    beacon = Column(INTEGER(10))
    initial_delay = Column(INTEGER(10))
    comms_http = Column(INTEGER(1))
    comms_dns = Column(INTEGER(1))
    comms_binary = Column(INTEGER(1))
    # last_check_in = Column(INTEGER(13))
    # unique_implant_key = Column(INTEGER(16), unique=True)

class GeneratedImplants(Base):
    __tablename__='generated_implants'
    unique_implant_id = Column(INTEGER(16), unique=True,nullable=False, primary_key=True)
    last_check_in = Column(INTEGER(16))
    current_beacon = Column(INTEGER(16))
    iid = Column(INTEGER(11), ForeignKey("implants.iid"), nullable=False, index=True)
    generated_title = Column(String(255),nullable=False)

class ImplantLogs(Base):
    __tablename__='implant_logs'
    log_id = Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    cid = Column(INTEGER(11), nullable=False, index=True)
    uid =Column(INTEGER(11), nullable=False, index=True)
    uik=Column(INTEGER(11), nullable=False, index=True)
    time =Column(INTEGER(11), nullable=False, index=True)
    log_entry =Column(String(255), nullable=False)

class Campaigns(Base):
    __tablename__='campaigns'
    cid = Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    title = Column(String(255), nullable=False, unique=True)
    created =Column(INTEGER(11), nullable=False, index=True)
    description = Column(String(255))

class CampaignUsers(Base):
    __tablename__='campaign_users'
    auto_id = Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    cid = Column(INTEGER(11),ForeignKey("campaigns.cid"), nullable=False, index=True )
    uid = Column(INTEGER(11), nullable=False, index=True)
    permissions =Column(TINYINT(1),nullable=False, server_default=text("'0'"))
    #write =Column(TINYINT(1),nullable=False, server_default=text("'0'"))

class AppLogs(Base):
    __tablename__='app_logs'
    log_id = Column(INTEGER(16), primary_key=True, index=True, nullable=False)
    type = Column(String(255), nullable=False)
    data = Column(String(255),nullable=False)