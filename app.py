from flask import Flask, g
import models

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
def after_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    

## The default URL 
@app.route('/')
def index():
    return 'hi'

## Run the app when the program starts
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
    
