import models 

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

users = Blueprint('users', __name__)


##INDEX
@users.route('/', methods=["GET"])
def get_all_users():
    try:
        users = [model_to_dict(user) for user in models.User.select()]
        print(users)
        return jsonify(data=users, status={"code": 200, "message": "Success retriving users"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error retrieving users."})
    
##NEW

##DELETE

##UPDATE

##CREATE
@users.route("/", methods=["POST"])
def create_user():
    payload = request.get_json()
    print(type(payload), 'payload')
    user = models.User.create(**payload)
    print(user.__dict__)
    print(dir(user))
    print(model_to_dict(user), 'model to dict')
    user_dict = model_to_dict(user)
    return jsonify(data=user_dict, status={"code": 201, "message": "User successfully created"})

##EDIT

##SHOW