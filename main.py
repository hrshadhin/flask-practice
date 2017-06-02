from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from flask_httpauth import HTTPBasicAuth


#app init
app = Flask(__name__)
#api init
api = Api(app, prefix="/api/v1")
auth = HTTPBasicAuth()


#subscribe user list of dict
users = [
    {'email': 'hello@hrshadhin.me', 'name': 'Shadhin', 'id': 1}
]

USER_DATA = {
    "admin": "password"
}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

#healper function to get user from list
def get_user_by_id(user_id):
    for x in users:
        if x.get("id") == int(user_id):
            return x

#validate user inputs for api
subscriber_request_parser = RequestParser(bundle_errors=True)
subscriber_request_parser.add_argument("name", type=str, required=True, help="Name has to be valid string")
subscriber_request_parser.add_argument("email", required=True)
subscriber_request_parser.add_argument("id", type=int, required=True, help="Please enter valid integer as ID")



#subscriber collection
class SubscriberCollection(Resource):
    @auth.login_required
    def get(self):
        return users, 200

    @auth.login_required
    def post(self):
        args = subscriber_request_parser.parse_args()
        users.append(args)
        return {"msg": "Subscriber added", "subscriber_data": args}, 201

#single subscriber
class Subscriber(Resource):

    @auth.login_required
    def get(self, id):
        user = get_user_by_id(id)
        if not user:
            return {'error': 'User not found!'}, 404
        return user, 302

    @auth.login_required
    def put(self, id):
        args = subscriber_request_parser.parse_args()
        user = get_user_by_id(id)
        if user:
            users.remove(user)
            users.append(args)
        return args, 202

    @auth.login_required
    def delete(self, id):
        user = get_user_by_id(id)
        if user:
            users.remove(user)

        return None, 204


#api endpoints
api.add_resource(SubscriberCollection, '/subscribers')
api.add_resource(Subscriber, '/subscribers/<int:id>')

#run the app
if __name__ == '__main__':
    app.run(debug=True)