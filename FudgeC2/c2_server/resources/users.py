from flask_restful import Resource
from flask import request


class Users(Resource):
    people = [
        {"username": "john", "email": "john@moozle.wtf", "id": 1, "state":"active"},
        {"username": "bob", "email": "bob@moozle.wtf", "id": 2, "state":"active"}
    ]
    def get(self):
        # Return a list of
        print("aaaaaaaa")
        return {"data":self.people}

    def post(self, gid=None):
        a = {}
        print(request.form)
        try:
            a['username'] = request.form['username']
            a['email'] = request.form['email']
            a['id'] = len(self.people)
            a['state'] = 'active'
            print(a)
            self.people.append(a)
            return {"data":{"msg":"success"}}
        except Exception as E:
            print(f":::{E}")
        return {"error":"400"}, 400
