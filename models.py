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
    iid = Column(INTEGER(11), nullable=False, index=True)
    log_entry = Column(String(255), nullable=False, unique=True)
    time = Column(INTEGER(11), nullable=False, index=True)

class Implants(Base):
    __tablename__='implants'
    iid=Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    implant_key = Column(String(255), nullable=False, unique=True)
    title = Column(String(255),nullable=False)
    cid = Column(INTEGER(11), nullable=False, index=True )
    file_hash=Column(String(255), nullable=True)
    filename=Column(String(255), nullable=True, unique=True)
    callback_url = Column(String(255), nullable=False, server_default=text("127.0.0.1"))
    description = Column(String(255))
    beacon = Column(INTEGER(10))
    initial_delay = Column(INTEGER(10))
    comms_http = Column(INTEGER(1))
    comms_dns = Column(INTEGER(1))
    comms_binary = Column(INTEGER(1))


class ImplantLogs(Base):
    __tablename__='implant_logs'
    log_id = Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    cid = Column(INTEGER(11), nullable=False, index=True)
    uid =Column(INTEGER(11), nullable=False, index=True)
    iid =Column(INTEGER(11), nullable=False, index=True)
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
    cid = Column( INTEGER(11),ForeignKey("campaigns.cid"), nullable=False, index=True, )
    uid = Column(INTEGER(11), nullable=False, index=True)
    read =Column(TINYINT(1), server_default=text("'0'"))
    write =Column(TINYINT(1), server_default=text("'0'"))

