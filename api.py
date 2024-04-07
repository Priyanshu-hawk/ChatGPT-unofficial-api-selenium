from flask import Flask, request
from flask_restful import Resource, Api
from flask_autoindex import AutoIndex
from api_backend import * 
import json
from utils import update_remote_ip_ngrok_mongo
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

api = Api(app)

class SingleQ(Resource):
    def get(self):
        req_json = json.loads(request.data.decode('utf-8'))
        text = req_json['prompt']
        return {"response": make_gpt_request(text)}


api.add_resource(SingleQ, '/singleQuery')

if __name__ == '__main__':
    port = 5000
    try:
        update_remote_ip_ngrok_mongo(os.getenv("MONGO_DB_NAME"), os.getenv("MONGO_COLLECTION_NAME"),port=5000 , currStatus=1)
        start_chat_gpt()
        app.run(debug=False, port=5000)
    except KeyboardInterrupt as e:
        print("KeyboardInterrupt detected, exiting...")
    finally:
        stop_chat_gpt()
        update_remote_ip_ngrok_mongo(os.getenv("MONGO_DB_NAME"), os.getenv("MONGO_COLLECTION_NAME"), port=5000, currStatus=0)