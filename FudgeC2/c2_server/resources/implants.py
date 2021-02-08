import logging
from flask_restful import Resource, reqparse
from flask import request
from flask_login import current_user, login_required

from FudgeC2.Implant.ImplantFunctionality import ImplantFunctionality
from FudgeC2.Data.Database import Database
from FudgeC2.Implant.Implant import ImplantSingleton

implant_functionality = ImplantFunctionality()
db = Database()
logger = logging.getLogger(__name__)
implant_obj = ImplantSingleton.instance

class Implants(Resource):
    method_decorators = [login_required]

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('campaign_id', type=int, help='Campaign IDs are numeric.')
        args = parser.parse_args()

        processed_implants = []
        # Return a list of all implants the user has access to.
        a = db.implant.get_all_implants_by_user(current_user.user_email)
        print(args)
        if args['campaign_id'] is not None:
            for index, value in enumerate(a):
                if value['campaign_id'] == args['campaign_id']:
                    processed_implants.append(value)
            return processed_implants
        else:
            return a

class ImplantTemplates(Resource):
    # Returns the name and id of all implant templates for the specified campaign
    def get(self, campaign_id):
        if db.campaign.Verify_UserCanAccessCampaign(current_user.user_email, campaign_id) is not True:
            return [], 401
        list_of_implant_templates = db.implant.get_implant_templates_by_campaign_id(campaign_id)
        campaigns = {"data": []}
        for template in list_of_implant_templates:
            try:
                campaigns['data'].append({"id":template['iid'], "name":template['title']})
            except Exception as E:
                logger.warning(f"Implant template missing key/pair: {E}")
        return campaigns

class ImplantDetails(Resource):
    method_decorators = [login_required]
    # Return the configuration of an implant
    def get(self, implant_id):
        # Take UID and return info on it.
        campaign_id = db.campaign.get_campaign_id_from_implant_id(implant_id)
        if db.campaign.Verify_UserCanReadCampaign(current_user.user_email, campaign_id) is False:
            return {"message": "Insufficient permissions"}

        implant = db.implant.get_implant_information(implant_id)
        # Create simplfied dictionary with key attributes.
        data = {
            "generated_title": implant['generated_title'],
            "current_beacon": implant['current_beacon'],
            "unique_implant_id": implant['unique_implant_id'],
            "callback_url": implant['callback_url'],
            "description": implant['description'],
            "initial_delay": implant['initial_delay']
        }

        return {"data": data}


class ImplantRegistered(Resource):
    method_decorators = [login_required]
    def get(self):
        pass

class ImplantResponses(Resource):
    method_decorators = [login_required]
    def get(self, implant_id):
        # get all implant responses (pagination will be implemented later
        response_list = []
        campaign_id = db.campaign.get_campaign_id_from_implant_id(implant_id)
        if db.campaign.Verify_UserCanAccessCampaign(current_user.user_email, campaign_id):
            response_list = db.implant.get_implant_responses(implant_id)

        return {"data": response_list}

class ImplantExecute(Resource):
    method_decorators = [login_required]
    def get(self, implant_id):
        # Returns a list of implants commands:
        campaign_id = db.campaign.get_campaign_id_from_implant_id(implant_id)
        if db.campaign.Verify_UserCanWriteCampaign(current_user.user_email, campaign_id) is not True:
            return {"message": "You do no have sufficient access rights."}, 403
        # Can user return execute commands? No Return a 401?

        # Get implants modules:

        imp_func = implant_functionality.command_listing()
        return {"data": imp_func}

    def post(self, implant_id):
        # Register a command to be executed.
        rj = request.json
        command_type = rj.get("type", None)
        command_args = rj.get("args", None)
        command_dict = {"type": command_type, "args":command_args}
        if implant_functionality.validate_pre_registered_command(command_dict):
            campaign_id = db.campaign.get_campaign_id_from_implant_id(implant_id)
            response = implant_obj.add_implant_command_to_server(current_user.user_email,
                                                                 campaign_id,
                                                                 implant_id,
                                                                 command_dict)
            if response:
                return {"message": "Command successfully registered."}, 201

        return {"message": "Command registration failed"}, 401