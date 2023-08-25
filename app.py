from flask import Flask, g, request
import models
from flask_cors import CORS
from resources.users import users
from flask_login import LoginManager
import os



SECRET_KEY = 'azore_lou_cow'
DEBUG = True
PORT = 8000

## Initialize site
app = Flask(__name__)
app.secret_key= SECRET_KEY

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

app.register_blueprint(users, url_prefix='/api/v1/users')
    

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
    