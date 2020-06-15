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
        s = smtplib.SMTP(
            host=data['host'],
            port=data['port'])
        if state:
            try:
                s.starttls()
                s.login(data['email_account'], data['email_password'])
                if self.test_conn_open(s):
                    self.email = s
                    self.enable = True
            except Exception as e:
                logger.warning(f"Email configuration attempted and failed: {e}")
                pass

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
    def configure_email_client(self, host, port, email_account, password, from_address=None, check=False):
        # print("--",host,port,email_account,password,from_address, check)
        # TODO -- Get existing data and see what we're missing usr may only submit a single data point?
        state, data = db.email.get_full_email_server_configuration()

        s = smtplib.SMTP(
            host=host,
            port=port)
        try:
            s.starttls()
            s.login(email_account, password)
            if self.test_conn_open(s):
                if check:
                    return True, "Test successful."
                self.email = s
                print(db.email.set_email_server_configuration(host, port, email_account, password, from_address))
                logger.debug("Email configuration changed.")
                self.enable = True
                return True, "Configuration successful"
        except Exception as e:
            logger.warning(f"SMTP configuration for {email_account}@{host}:{port} failed. Reason: {e}")
            return False, f"SMTP configuration for {email_account}@{host}:{port} failed. Reason: {e}"

    @requires_enabled
    def send_email(self, to, msg):
        state, email_config = db.email.get_full_email_server_configuration()
        msg = MIMEText(msg)
        msg['Subject'] = 'New User Added'
        msg['From'] = email_config['from_address']
        msg['To'] = to

        try:
            self.email.sendmail(email_config['from_address'], to, msg.as_string())
            self.email.quit()
            return True
        except Exception as e:
            logger.warning(f"Sending email to: {to} failed. STMP config: {e}")
            return False
