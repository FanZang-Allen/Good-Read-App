""" This file is part of Good Read Web Scraper

DataBase class connect to the cloud mongodb database using key stored in dotenv file
Contain useful operation functions of the database
"""
import os
import json
import string
import certifi
import pymongo
from dotenv import load_dotenv
import common_utility


class DataBase:

    def __init__(self):
        """
        Connect to cloud database, store in instance variable
        """
        load_dotenv()
        self.client = pymongo.MongoClient(os.getenv('MONGODB_KEY'), tlsCAFile=certifi.where())
        self.database = self.client['GoodRead']

    def clear_collection(self, collection_name: string):
        """
        Clear the given collection in the database
        :param collection_name: name of collection to clear
        :return: None
        """
        if collection_name in self.database.list_collection_names():
            self.database[collection_name].delete_many({})
        else:
            print("Collection not exist")

    def add_data(self, data: dict, collection_name: string):
        """
        Add data to collection. If data id already exist, update the corresponding documentation
        :param data: data in python dict
        :param collection_name: should exist in database
        :return: True if success
        """
        if collection_name not in self.database.list_collection_names():
            print("Collection not exist")
            return False

        curr_collection = self.database[collection_name]
        if curr_collection.count_documents({'id': data['id']}, limit=1) != 0:
            self.update_data(data, collection_name)
        else:
            curr_collection.insert_one(data)
            print(collection_name + ' with id:' + str(data['id']) + ' is created in database')
        return True

    def update_data(self, data: dict, collection_name: string):
        """
        Update documentation using info in data dict
        :param data: data in python dict
        :param collection_name: should exist in database
        :return:True if success
        """
        if collection_name not in self.database.list_collection_names():
            print("Collection not exist")
            return False

        curr_collection = self.database[collection_name]
        curr_id = data['id']
        for key in data:
            if key != 'id':
                curr_collection.update_one({'id': curr_id}, {"$set": {key: data[key]}})
        print(collection_name + ' with id:' + str(data['id']) + ' is updated in database')
        return True

    def delete_data(self, collection_name: str, data_id: str):
        """
        Delete documentation with given id
        :param collection_name: should exist in database
        :param data_id: id of documentation
        :return:True if success
        """
        if collection_name not in self.database.list_collection_names():
            print("Collection not exist")
            return False

        curr_collection = self.database[collection_name]
        curr_collection.delete_one({'id': data_id})
        return True

    def export_data_json(self, file_name: string):
        """
        Export all data stored in database to a json file
        :param file_name: stored json file path
        :return:None
        """
        export_dict = {}

        for collection_name in self.database.list_collection_names():
            collection_list = []
            info_cursor = self.database[collection_name].find({}, {'_id': 0})
            for info in info_cursor:
                collection_list.append(info)
            export_dict[collection_name] = collection_list

        with open(file_name, 'w') as export_file:
            json.dump(export_dict, export_file, indent=2)
            print("data has been export to " + file_name)

    def load_json_data(self, file_name: string):
        """
        Load data in a valid json file to database
        :param file_name: path to file to read
        :return: None
        """
        result = common_utility.check_valid_json_file(file_name)
        if result != file_name:
            print(result)
            return
        with open(file_name) as loaded_file:
            data = json.load(loaded_file)
            for collection_name in data:
                info_list = data[collection_name]
                for info in info_list:
                    self.add_data(info, collection_name)
