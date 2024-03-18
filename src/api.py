from flask_restful import Resource
from flask import request
import json
import pandas as pd
import os
from werkzeug.utils import secure_filename
from src.visualize import Generate
import os

model = Generate()


class Visualize(Resource):
    def post(self):
        try:
            data = json.loads(request.data)
        except:
            return { "message": "Error in parsing request body" }

        query = data['query']
        filename = data['file']
        df = pd.read_pickle(os.path.join(os.getcwd(),'dataframe', filename))

        try:
            return model.generate(query,df,filename)
        except:
            return {
                "result_type": "graph",
                "data": {
                    "labels": [],
                    "label": "Try different query",
                    "data": []
                }
            }


class Files(Resource):
    def get(self):
        try:
            return {
                "files": os.listdir("./dataframe")
            }
        except:
            return {
                "files": []
            }

class Upload(Resource):
    def post(self):
        try:
            file = request.files['file']
            filename = secure_filename(file.filename)
            df = pd.read_csv(file)
            df.to_pickle(os.path.join(os.getcwd(),'dataframe', filename))
            return {
                "message": "success"
            }
        except:
            return {
                "message": "failed"
            }