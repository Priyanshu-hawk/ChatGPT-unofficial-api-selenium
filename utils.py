import ngrok
from datetime import datetime
import firebase_admin
import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

BASE_CURR_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

class mongo_db_connection():
    def __init__(self, db_name):
        self.uri = os.getenv("MONGO_URI")
        self.ca = certifi.where()
        self.client = MongoClient(self.uri, tlsCAFile=self.ca)
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.db = self.client[db_name]

    def insert_one(self, collection_name, item):
        collection = self.db[collection_name]
        mongo_id = collection.insert_one(item)
        return mongo_id.inserted_id
    
    def get_all(self, collection_name):
        collection = self.db[collection_name]
        all_items = collection.find()
        return all_items

    def delete_item(self, collection_name, item):
        collection = self.db[collection_name]
        collection.delete_one(item)

    def find_one_by_uiqu_id(self, collection_name, id):
        all_items = self.get_all(collection_name)
        for item in all_items:
            if id in item:
                return item
        return None

    def is_uiqu_id_exist(self, collection_name, id):
        all_items = self.get_all(collection_name)
        for item in all_items:
            if id in item:
                return True
        return False
    
    def update_by_mongo_id(self, collection_name, mongo_id, new_json):
        collection = self.db[collection_name]
        collection.update_one({"_id": mongo_id}, {"$set": new_json})


def update_remote_ip_ngrok_mongo(db_name, collection, port, currStatus=0):
    """
    currStatus: 1 to start server
                0 to stop server
    """
    
    conn = mongo_db_connection(db_name)

    ##getting all data
    for i in conn.get_all(collection):
        mongo_id = i['_id']

    if currStatus == 1:
        listner = ngrok.forward(addr="localhost:"+str(port),authtoken=os.getenv("NGROK_AUTH_TOKEN"))


        conn.update_by_mongo_id(collection, mongo_id, {"ip_ep": listner.url(), "time": datetime.now(), "type": "server", "status": 1})
        
        print(listner.url())
    else:
        conn = mongo_db_connection(db_name)

        ##getting all data
        for i in conn.get_all(collection):
            mongo_id = i['_id']

        conn.update_by_mongo_id(collection, mongo_id, {"status": 0})
        

