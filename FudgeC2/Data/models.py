# coding: utf-8
import os

from sqlalchemy import Column, ForeignKey, String, text, create_engine, PickleType,  DateTime  # , Table, Text, Index, Date, DateTime, Float,
from sqlalchemy.dialects.mysql import INTEGER  # MEDIUMTEXT, TINYINT, VARCHAR, BIGINT
from sqlalchemy.ext.declarative import declarative_base

from Storage.settings import Settings

Base = declarative_base()
metadata = Base.metadata


import json
import sqlalchemy
from sqlalchemy.types import TypeDecorator

SIZE = 256

class TextPickleType(TypeDecorator):

    impl = sqlalchemy.Text(SIZE)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


# TODO: Create a resources log table.
class Users(Base):
    __tablename__ = 'users'
    uid = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    user_email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    last_login = Column(String(255), nullable=False)
    authenticated = Column(String, server_default=text("False"))
    active_account = Column(String(), default=1)
    admin = Column(String(255), nullable=False)
    first_logon = Column(INTEGER(1), nullable=False, default=0)
    first_logon_guid = Column(String(32), nullable=False, default="0")

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

class EmailClient(Base):
    __tablename__ = "email_client"
    id = Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    email_account = Column(String)
    email_password = Column(String)
    from_address = Column(String)
    host  = Column(String)
    port  = Column(String)

class ImplantTemplate(Base):
    __tablename__ = 'implant_template'
    iid = Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    stager_key = Column(String(255), nullable=False, unique=True)
    title = Column(String(255), nullable=False, unique=True)
    cid = Column(INTEGER(11), nullable=False, index=True)
    callback_url = Column(String(255), nullable=False)
    description = Column(String(255))
    beacon = Column(INTEGER(10), nullable=False)
    kill_date = Column(String(32), default=None)
    initial_delay = Column(INTEGER(10))
    network_profiles = Column(TextPickleType(), nullable=False)
    obfuscation_level = Column(INTEGER(1), nullable=False)
    encryption = Column(TextPickleType(), nullable=False)
    operating_hours = Column(TextPickleType(), nullable=False)


class GeneratedImplants(Base):
    __tablename__ = 'generated_implants'
    unique_implant_id = Column(String(16), unique=True, nullable=False, primary_key=True)
    last_check_in = Column(INTEGER(16))
    last_check_in_protocol = Column(String())
    current_beacon = Column(INTEGER(16))
    iid = Column(INTEGER(11), ForeignKey("implant_template.iid"), nullable=False, index=True)
    generated_title = Column(String(255), nullable=False)
    time = Column(INTEGER(16), nullable=False)
    implant_copy = Column(String())
    delivered_payload = Column(String()) # If encryption or 3rd party obfuscation is used


class ImplantCommands(Base):
    __tablename__ = 'implant_commands'
    log_id = Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    cid = Column(INTEGER(11), nullable=False, index=True)
    uid = Column(INTEGER(11), nullable=False, index=True)
    uik = Column(INTEGER(11), nullable=False, index=True)
    time = Column(INTEGER(11), nullable=False, index=True)
    log_entry = Column(TextPickleType(), nullable=False)
    read_by_implant = Column(INTEGER(16), nullable=False, server_default=text("0"))
    c2_protocol = Column(String(128))
    command_id = Column(String(128))


class ImplantResponse(Base):
    __tablename__ = 'implant_response'
    log_id = Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    cid = Column(INTEGER(11), nullable=False, index=True) # This can be removed as implant_id should be the only linking element
    uik = Column(INTEGER(11), nullable=False, index=True)
    log_entry = Column(String(255), nullable=False)
    time = Column(INTEGER(11), nullable=False, index=True)
    command_id = Column(String(128))


class Campaigns(Base):
    __tablename__ = 'campaigns'
    cid = Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    title = Column(String(255), nullable=False, unique=True)
    created = Column(INTEGER(11), nullable=False, index=True)
    description = Column(String(255))


class CampaignUsers(Base):
    __tablename__ = 'campaign_users'
    auto_id = Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    cid = Column(INTEGER(11), ForeignKey("campaigns.cid"), nullable=False, index=True)
    uid = Column(INTEGER(11), nullable=False, index=True)
    permissions = Column(INTEGER(1), nullable=False, default=0)


class AppLogs(Base):
    __tablename__ = 'app_logs'
    log_id = Column(INTEGER(16), primary_key=True, index=True, nullable=False)
    time = Column(String(), nullable=False)
    type = Column(String(255), nullable=False)
    data = Column(String(255), nullable=False)


class CampaignLogs(Base):
    __tablename__ = 'campaign_logs'
    auto_id = Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    user = Column(INTEGER(8), nullable=False)
    campaign = Column(INTEGER(8), nullable=False)
    time = Column(INTEGER(32), nullable=False)
    log_type = Column(String(32), nullable=False)
    entry = Column(TextPickleType(), nullable=False)


class HostData(Base):
    __tablename__ = "host_data"
    auto_id = Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    unique_implant_key = Column(INTEGER(), ForeignKey(GeneratedImplants.unique_implant_id))
    ip_address = Column(String())


class Listeners(Base):
    __tablename__ = 'listeners'
    auto_id = Column(INTEGER(), nullable=False, index=True, primary_key=True)
    name = Column(String())
    state = Column(INTEGER())  # This can be removed.
    protocol = Column(INTEGER())
    port = Column(INTEGER())
    auto_run = Column(INTEGER())


# -- Generate an empty database if no database is found.
# --    additional checks for file existence would be sensible first

path = os.getcwd() + "/Storage/"
engine = create_engine(f"sqlite:///{path}/{Settings.database_name}?check_same_thread=False", echo=False)
Base.metadata.create_all(engine)
