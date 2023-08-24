import models 
from flask import Blueprint, jsonify, request
from flask_login import LoginManager, login_user, login_required, current_user, logout_user # Import user_loader
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist


users = Blueprint('users', __name__)

login_manager = LoginManager()  # Create a LoginManager instance


##INDEX
@users.route('/', methods=["GET"])
def get_all_users():
    try:
        users = [model_to_dict(user) for user in models.User.select()]
        print(users)
        return jsonify(data=users, status={"code": 200, "message": "Success retriving users"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error retrieving users."})
    

##LOGIN
@users.route("/login", methods=["POST"])
def login():
    payload=request.get_json()
    print(payload)
    try:
        user=models.User.get(models.User.username == payload['username'])
        if user.password == payload["password"]:
            login_user(user)
            user_dict = model_to_dict(user)
            return jsonify(data=user_dict, status={"code": 200, "message": "Login successful"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Invalid credentials."})
    except DoesNotExist:
        return jsonify(data={}, status={"code":401, "message": "Invalid credentials."})
            
##CREATE/REGISTER
@users.route("/register", methods=["POST"])
def register_user():
    payload = request.get_json()
    print(type(payload), 'payload')
    try:
        user = models.User.create(username=payload['username'], email=payload['email'], password=payload['password'])
        print(user.__dict__)
        print(dir(user))
        print(model_to_dict(user), 'model to dict')
        user_dict = model_to_dict(user)
        return jsonify(data=user_dict, status={"code": 201, "message": "User successfully created"})
    except Exception as e:
        return jsonify(data={}, status={"code": 400, "message": str(e)})


##SHOW/CURRENT USER
@users.route("/current_user", methods=["GET"])
@login_required
def current_user():
    user_dict = model_to_dict(current_user)
    return jsonify(data=user_dict, status={"code": 200, "message": "Current user retrieved"})

## LOGOUT
@users.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify(data={}, status={"code": 200, "message": "Logout successful"})
 