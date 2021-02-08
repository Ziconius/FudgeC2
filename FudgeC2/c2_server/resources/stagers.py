import logging
from flask_restful import Resource, reqparse
from flask_login import login_required, current_user

from FudgeC2.Data.Database import Database
from FudgeC2.Stagers.stager_generation import StagerGeneration

logger = logging.getLogger(__name__)
sg = StagerGeneration()
db = Database()


class Stagers(Resource):
    method_decorators = [login_required]

    #get a list of all implants by Campaign ID

    def get(self, implant_template_id):

        result = {"data":sg.get_stager_options()}

        return result, 200


class StagerGeneration(Resource):
    method_decorators = [login_required]

    def get(self, implant_template_id):
        # db.implant.
        pass
        return 200
