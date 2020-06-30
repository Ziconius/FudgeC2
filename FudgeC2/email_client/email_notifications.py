# This class is responsible for creating the email message, to and from addresses before handing the information to
#   the EmailClient class to send the email. This class will also answer any queries about the state of the EmailClient
#   configuration
#
# All public methods will return a boolean response and nothing else. Any errors will be logged using the Logger class
#   ensuring a consistent style.
#
# The EmailNotifications class is not responsible for the authorisation, and calls should be authorised before any
#   methods are called.
#
import logging

from email_client.email_client import EmailClient

logger = logging.getLogger(__name__)
ec = EmailClient()


class EmailNotification:

    def email_notification_configuration(self):
        if ec.enable:
            return True
        elif ec.enable is False:
            return False
        else:
            logger.critical("EmailClient class is returning a non-boolean value for 'EmailClient.enable'")
        return ec.enable

    def send_email_new_user_account(self, name, email, password):
        # This will
        # TODO: Additional configurable field to override hardcoded value.
        server_address = "https://127.0.0.1:5001"
        #
        email_text = f"""
Hi {name},

Your admin has created you an operator account on your companies FudgeC2 server.

You can login with your username or email address here:
 {server_address}
 
 Your temp password is: {password}
 
 for more information on FudgeC2 and it's capabilities see:
 https://github.com/Ziconius/FudgeC2/
 
 N.b Depending on your network configuration the login portal may not be accessible from the login URL.
 
 Thank you,
 """
        result = ec.send_email(email, email_text)
        return result
