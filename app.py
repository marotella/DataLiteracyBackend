from flask import Flask

DEBUG = True
PORT = 8000

## Initialize site
app = Flask(__name__)

## The default URL 
@app.route('/')
def index():
    return 'hi'

## Run the app when the program starts
if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
    
