# Sender
import smtplib
import logging
from email.mime.text import MIMEText
import sys

[sys.path.append(i) for i in ['.', '..']]
logger = logging.getLogger(__name__)

try:
    from Data.Database import Database
except:
    from FudgeC2.Data.Database import Database

db = Database()


class EmailClient:
    # set up the SMTP server
    enable = False
    # Configured email object.
    email = False

    def __init__(self):
        # Setup email config if one exists.
        state, data = db.email.get_full_email_server_configuration()
        if state:
            conf_success, data = self._configure_email_client(data['username'], data['email_password'], data['host'], data['port'], data['encryption'])
            if conf_success:
                self.email = data
                self.enable = True
            else:
                logger.warning(f"__init__() failed: {data}")

    def _configure_email_client(self, username, password, host, port, encryption):
        try:
            if encryption == "SSL":
                s = smtplib.SMTP_SSL(
                    host=host,
                    port=port,
                )
            else:
                s = smtplib.SMTP(
                    host=host,
                    port=port,
                )
                s.login(username, password)
            connection_test = self.test_conn_open(s)
            if connection_test:
                return True, s
            else:
                return False, "Error"
        except Exception as E:
            print(E)
            return None, f"{E}"


    # Ensure the email functionality has been configured before attempting to send any messages.
    def requires_enabled(func):
        def decorate(self, *args, **kwargs):
            if self.enable is not False:
                func(self, *args, **kwargs)
            else:
                return False
        return decorate

    # Check the connection is established and valid -
    def test_conn_open(self, conn):
        try:
            status = conn.noop()[0]
        except:  # smtplib.SMTPServerDisconnected
            status = -1
        return True if status == 250 else False

    # Should require admin privs. returns True, msg || False msg
    def configure_email_client(self, host, port, encryption, username, password, from_address=None, check=False):
        # print("--",host,port,email_account,password,from_address, check)
        # TODO -- Get existing data and see what we're missing usr may only submit a single data point?
        # state, data = db.email.get_full_email_server_configuration()

        conf_success, data = self._configure_email_client(username, password, host, port, encryption)
        if conf_success:
            if check:
                return True, "Test successful."
            save_record = db.email.set_email_server_configuration(host, port, encryption, username, password, from_address)
            if save_record:
                self.email = data
                self.enable = True
                return True, "Configuration successful."
            else:
                return False, "Database error."
        else:
            logger.warning(f"SMTP configuration for {username}@{host}:{port} failed. Reason: {data}")
            return False, f"SMTP configuration for {username}@{host}:{port} failed. Reason: {data}"

        # try:
        #     s = smtplib.SMTP(
        #         host=data['host'],
        #         port=data['port'])
        #     s.ehlo()
        #     s.starttls()
        # except Exception as E:
        #     logger.warning(f"Host:{data['host']}, port: {data['port']}, Exception{E}")
        #     return
        # try:
        #     s.starttls()
        #     s.login(email_account, password)
        #     if self.test_conn_open(s):
        #         if check:
        #             return True, "Test successful."
        #         self.email = s
        #         print(db.email.set_email_server_configuration(host, port, email_account, password, from_address))
        #         logger.debug("Email configuration changed.")
        #         self.enable = True
        #         return True, "Configuration successful"
        # except Exception as e:
        #     logger.warning(f"SMTP configuration for {email_account}@{host}:{port} failed. Reason: {e}")
        #     return False, f"SMTP configuration for {email_account}@{host}:{port} failed. Reason: {e}"

    @requires_enabled
    def send_email(self, to, msg):
        state, email_config = db.email.get_full_email_server_configuration()
        msg = MIMEText(msg)
        msg['Subject'] = 'New User Added'
        msg['From'] = email_config['from_address']
        msg['To'] = to
        print(msg)
        try:
            self.email.sendmail(email_config['from_address'], to, msg.as_string())
            self.email.quit()
            return True
        except Exception as e:
            logger.warning(f"Sending email to: {to} failed. STMP config: {e}")
            return False
