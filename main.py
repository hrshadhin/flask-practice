from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from flask_jwt import JWT, jwt_required

#app init
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-super-secret-key-here'
#api init
api = Api(app, prefix="/api/v1")

#subscribe subscriber list of dict
subscribers = [
    {'email': 'hello@hrshadhin.me', 'name': 'Shadhin', 'id': 1}
]
#user authentication functions
USER_DATA = {
    "admin": "password"
}
class user(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "user(id='%s')" % self.id


def verify(username, password):
    if not (username and password):
        return False
    if USER_DATA.get(username) == password:
        return user(id=123)

def identity(payload):
    user_id = payload['identity']
    return {"user_id": user_id}

jwt = JWT(app,verify,identity)


#healper function to get subscriber from list
def get_subscriber_by_id(subscriber_id):
    for x in subscribers:
        if x.get("id") == int(subscriber_id):
            return x

#validate subscriber inputs for api
subscriber_request_parser = RequestParser(bundle_errors=True)
subscriber_request_parser.add_argument("name", type=str, required=True, help="Name has to be valid string")
subscriber_request_parser.add_argument("email", required=True)
subscriber_request_parser.add_argument("id", type=int, required=True, help="Please enter valid integer as ID")



#subscriber collection
class SubscriberCollection(Resource):
    @jwt_required()
    def get(self):
        return subscribers, 200

    @jwt_required()
    def post(self):
        args = subscriber_request_parser.parse_args()
        subscribers.append(args)
        return {"msg": "Subscriber added", "subscriber_data": args}, 201

#single subscriber
class Subscriber(Resource):
    @jwt_required()
    def get(self, id):
        subscriber = get_subscriber_by_id(id)
        if not subscriber:
            return {'error': 'subscriber not found!'}, 404
        return subscriber, 302
    @jwt_required()
    def put(self, id):
        args = subscriber_request_parser.parse_args()
        subscriber = get_subscriber_by_id(id)
        if subscriber:
            subscribers.remove(subscriber)
            subscribers.append(args)
        return args, 202
    @jwt_required()
    def delete(self, id):
        subscriber = get_subscriber_by_id(id)
        if subscriber:
            subscribers.remove(subscriber)

        return None, 204


#api endpoints
api.add_resource(SubscriberCollection, '/subscribers')
api.add_resource(Subscriber, '/subscribers/<int:id>')

#run the app
if __name__ == '__main__':
    app.run(debug=True)