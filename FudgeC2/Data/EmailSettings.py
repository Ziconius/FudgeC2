import logging

from Data.models import EmailClient

logger = logging.getLogger(__name__)

class EmailSettings:

    def __init__(self, source_database, session):
        # TODO: Check session type
        self.Session = session
        self.db_methods = source_database

    def set_email_server_configuration(self, host, port, encryption, email_account, password, from_address):
        # This will contain full optional updates to all fields, and will only be triggered if the configuration is
        #   considered to be valid.
        # Check for existing record
        results = self.Session.query(EmailClient).all()
        if len(results) == 0:
            email_settings = EmailClient(
                username=email_account,
                email_password=password,
                from_address=from_address,
                host=host,
                port=port,
                encryption=encryption
            )
            self.Session.add(email_settings)
            try:
                self.Session.commit()
                return True

            except Exception as e:
                logger.exception(f"Error in set_email_server_configuration() SQLAlc error: {e}")
                return False
        # Update existing record
        self.Session.query(EmailClient).update(
            {"email_account": email_account,
            "email_password": password,
            "from_address": from_address,
            "host": host,
            "port": port,
            "encryption":encryption})
        self.Session.commit()
        pass

    def get_email_server_configuration(self, user):

        results = self.Session.query(EmailClient).all()
        if len(results) == 1:
            # We have a record to return
            r = results[0].__dict__
            del r['_sa_instance_state']
            del r['email_password']
            del r['id']

            return True, r

        elif len(results) == 0:
            return False, "No email configuration exists."
        else:
            logger.warning("There is more than one record for email clients. There should only be a single record.")
            return False, "Error occurred - more than one SMTP server configured"

    def get_full_email_server_configuration(self):
        # Returns everything including the encrypted password.
        results = self.Session.query(EmailClient).all()
        if len(results) == 1:
            # We have a record to return
            r = results[0].__dict__
            return True, r

        elif len(results) == 0:
            return False, "No email configuration exists"
        else:
            logger.warning("There is more than one record for email clients. There should only be a single record.")
            return False, "Error occurred - more than one SMTP server configured"

