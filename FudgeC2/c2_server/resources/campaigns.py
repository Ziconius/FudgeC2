from flask_restful import Resource

class Campaigns(Resource):
    def get(self, gid=None):
        # Return a list of
        return {"data":[{"name":"Campaign one","id":1,"description":"Basic campaign example"}]}
    def post(self):
        pass
