from pymongo import MongoClient
import json
from bson import json_util, ObjectId


class MongoODM:

    def __init__(self, port=27017, db_name='comments'):
        self.port = port
        self.conn = MongoClient('mongodb://dentzen_mongo_db')
        self.db = self.conn[db_name]

    def insert(self, collection_name, data):
        collection = self.db[collection_name]
        return collection.insert_one(data)

    def find_many(self, collection_name, parent_name, parent_id):

        if collection_name is None:
            return False

        collection = self.db[collection_name]

        data = collection.find({parent_name: parent_id})
        if not data:
            return False
        return [json.loads(json_util.dumps(obj)) for obj in data]

    def find_one(self, collection_name, parent_name, parent_id, comment_id):

        if collection_name is None:
            return False

        collection = self.db[collection_name]

        data = collection.find_one({parent_name: parent_id, '_id': ObjectId(comment_id)})
        if not data:
            return False
        return json_util.dumps(data)

    def update_one(self, collection_name, updated_data, comment_id):

        if collection_name is None:
            return False

        collection = self.db[collection_name]

        identifier = {"_id": ObjectId(comment_id)}
        for key, item in updated_data.items():
            if key == '_id':
                continue
            collection.update_one(identifier, {"$set": {key: item}})
        return True

    def delete_one(self, collection_name, comment_id):

        if collection_name is None:
            return False

        collection = self.db[collection_name]

        document = collection.delete_one({'_id': ObjectId(comment_id)})
        return document.acknowledged

