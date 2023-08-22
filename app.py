from flask import Flask, g, request
import models
from flask_cors import CORS
from resources.users import users

DEBUG = True
PORT = 8000

## Initialize site
app = Flask(__name__)

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

CORS(users, origins = ['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(users, url_prefix='api/v1/users')
    

## The default URL 
@app.route('/')
def index():
    return 'hi'

## Run the app when the program starts
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
    
