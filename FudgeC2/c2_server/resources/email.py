from flask_restful import Resource
from flask import request
from flask_login import current_user, login_required

from email_client.email_client import EmailClient

from Data.Database import Database
db = Database()
email_client = EmailClient()


# Endpoints for email configuration.
class Email(Resource):
    method_decorators = [login_required]

    def get(self, gid=None):
        # Return a list of
        print(type(current_user.admin))
        if current_user.admin != "1":
            return {"message": "Insufficient permissions"}, 403

        state, data = db.email.get_email_server_configuration(current_user.user_email)
        if state:
            return {"data": data}, 200
        else:
            return {"message": data}, 302

    def post(self):
        if current_user.admin != "1":
            return {"message": "Insufficient permissions"}, 403
        rj = request.json


        # Validate the contents of this and send to the email class
        server_email = rj.get("smtp_account", None)
        server_password = rj.get("password", None)
        server_host = rj.get("host", None)
        server_port = rj.get("port", None)
        server_encryption = rj.get("encryption", None)
        from_address = rj.get("from_address", None)
        check_config = rj.get("check_config", False)
        state, msg = email_client.configure_email_client(
            server_host,
            server_port,
            server_encryption,
            server_email,
            server_password,
            from_address,
            check_config)

        if state:
            return {"result": msg}, 201
        else:
            return {"result": msg}, 500

    def delete(self):
        pass


# Used to check which notification have been configured. Without the Email being configured no notifications will be sent.
class EmailNotifications(Resource):
    def get(self):
        pass


class EmailTest(Resource):
    def get(self):
        pass

    def post(self):
        # Not checking if configured. Need to check.
        rj = request.json
        to = rj.get("to", None)
        msg = rj.get("msg", None)
        response = email_client.send_email(to, msg)
        print(response)