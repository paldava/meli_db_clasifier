import logging

import pymongo
from bson import ObjectId


class MongoAPI:
    def __init__(self, data):
        self.client = pymongo.MongoClient('mongodb://root:Me1iCh411enge@mongodb:27017/')

        database = 'meli_db_clasifier'
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def read_by_id(self, id):
        return self.collection.find_one(ObjectId(id))

    def read_sorting_and_filtering_field(self, filter_field, value, sort_field, sort_type):
        return self.collection.find({filter_field: value}).sort(sort_field, sort_type)

    def write(self, data):
        logging.info('Writing Data')
        response = self.collection.insert_one(data)
        output = {'Status': 'Successfully Inserted',
                  'ID': str(response.inserted_id)}
        return output

    def write_many(self, data):
        logging.info('Writing Data')
        self.collection.insert_many(data)
        output = {'Status': 'Successfully Inserted'}
        return output
