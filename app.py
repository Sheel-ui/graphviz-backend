from flask import Flask
from flask_restful import Api
from src.api import *
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
api = Api(app)
CORS(app)
load_dotenv()


api.add_resource(Visualize, os.getenv('ENDPOINT'))
api.add_resource(Files, '/files')
api.add_resource(Upload, '/upload')

if __name__ == '__main__':
   app.run(port=os.getenv('PORT'),host=os.getenv('HOST'),debug=True)