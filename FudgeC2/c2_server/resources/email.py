from flask_restful import Resource
from flask import request
from flask_login import current_user, login_required

from email_client.email_client import EmailClient

from Data.Database import Database
db = Database()
email_client = email_client()

# Endpoints for email configuration.
class Email(Resource):
    method_decorators = [login_required]

    # @login_required
    def get(self, gid=None):
        # Return a list of
        state, data = db.email.get_email_server_configuration(current_user.user_email)
        if state:
            return {"data":data}, 200
        else:
            return {"message":data}, 302

    def post(self):
        rj = request.json
        # Validate the contents of this and send to the Meail class
        server_email = rj.get("server_email", None)
        server_password = rj.get("server_password", None)
        server_host = rj.get("server_host", None)
        server_port = rj.get("server_port", None)
        from_address = rj.get("server_from_addr", None)
        check_config= rj.get("check_config", False)
        print(f"State:\n{server_host}\n{server_port}\n{server_email}\n{server_password}\n{from_address}\n{check_config}")
        state, msg = email_client.configure_email_client(server_host, server_port, server_email, server_password, from_address, check_config)
        if state:
            return {"result":msg}, 200
        else:
            return {"result": msg}, 400

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
        email_client.send_email(to, msg)
