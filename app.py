from flask import Flask, g, request
import models
from flask_cors import CORS
from resources.users import users
from resources.students import students
from resources.criteria import placementCriteria
from resources.placementMatch import match
from flask_login import LoginManager
import os
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager


SECRET_KEY = 'azore_lou_cow'
DEBUG = True
PORT = 8000

## Initialize site
app = Flask(__name__)
app.secret_key= SECRET_KEY
app.config['JWT_SECRET_KEY'] = 'cow_lou_azore'
jwt = JWTManager(app)

##Database connection:
@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    
@app.after_request
def after_request(response):
    """Close to the database before each request."""
    if not g.db.is_closed():
        g.db.close()
        return response

login_manager = LoginManager(app)


CORS(users, origins = ['http://localhost:3000'], supports_credentials=True)
CORS(placementCriteria, origins = ['http://localhost:3000'], supports_credentials=True)
CORS(students, origins = ['http://localhost:3000'], supports_credentials=True)
CORS(match, origins = ['http://localhost:3000'], supports_credentials = True)

app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(students, url_prefix='/api/v1/students')
app.register_blueprint(placementCriteria, url_prefix='/api/v1/criteria')  
app.register_blueprint(match, url_prefix="/api/v1/match" )

## The default URL 
@app.route('/')
def index():
    return 'hi'

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return models.User.get_by_id(user_id)

## Run the app when the program starts
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
    
