from flask import Flask
from flask_cors import CORS
from routes import api
from waitress import serve

app = Flask(__name__)
CORS(app)

app.register_blueprint(api)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5001)
