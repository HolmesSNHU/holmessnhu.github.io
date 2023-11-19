#!/usr/bin/env python
# coding: utf-8

from pymongo import MongoClient
from pymongo import errors
from bson.objectid import ObjectId

class ClientDataCRUD(object):
    """ CRUD operations for CS499_client_database in MongoDB """

    def __init__(self, inputUser=None, inputPass=None):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        
        # The login credentials will be replaced in the future with a proper login database.
        USER = inputUser if inputUser is not None else 'admin'
        PASS = inputPass if inputPass is not None else 'root'
        HOST = 'localhost'
        PORT = 27017
        DB = 'CS499_client_database'
        # COL = 'accounts'
        
        #
        # Initialize Connection
        #
        
        # Make sure to follow industry standards with the implementation by adding exception handling and inline comments.
        try:
            self.client = MongoClient('mongodb://%s:%s@%s:%d/%s' % (USER,PASS,HOST,PORT,DB))
            self.database = self.client['%s' % (DB)]
            if self.database is not None:
                print(f"Connected to database: {DB}")
            else:
                print(f"Failed to connect to the {DB} database.")
            # self.collection = self.database['%s' % (COL)]         # Commenting this out since we'll be setting it later.
        
        except errors.ConnectionFailure as connectionError:
            print(f"Connection error: {connectionError}")
        except Exception as exception:
            print(f"An unexpected exception occurred while connecting to the database: {exception}")

# Complete this create method to implement the C in CRUD.
    def create(self, collectionName, data):
        # First, validate that the 'data' is present and 'collection' has been designated
        if data is not None and collectionName is not None:
            
            # Then attempt to insert it into the database.
            try:
                collection = self.database[collectionName]
                print(f"Attempting to access the collection: {collection}")
                insertResult = collection.insert_one(data)  # data should be dictionary
                # If successful, explicitly acknowledge success.
                if insertResult.acknowledged:
                    print("Insertion acknowledged by server.")
                    return True
                # If unsuccessful, explicitly acknowledge failure.
                else:
                    print("Insertion failed; server did not acknowledge document.")
                    return False
                
            except errors.OperationFailure as operationFailure:
                print(f"Operation failure: {operationFailure}")
            except Exception as exception:
                print(f"An unexpected exception occurred: {exception}")
        else:
            raise Exception("Nothing to save, because data parameter is empty")
            return False

# Create method to implement the R in CRUD.
    def read(self, collectionName, data):
        # First, validate that the 'data' is present.
        if data is not None and collectionName is not None:
            # Then attempt to read the requested data from the database.
            try:
                collection = self.database[collectionName]
                print(f"Attempting to access collection: {collection}")
                # This should return a list that either contains the results or is empty
                return [entry for entry in collection.find(data)]
            
            except errors.OperationFailure as operationFailure:
                print(f"Operation failure: {operationFailure}")
                # If the return fails, we want to gracefully handle it by ensuring the empty list returns.
                return []
            except Exception as exception:
                print(f"An unexpected exception occurred: {exception}") 
                return []
        else:
            raise Exception("No entry can be returned due to the data parameter being empty or no collection being specified.")
            return []
        
# Create method to implement the U in CRUD.
    def update(self, collectionName, target, updatedData):
        # First, validate that the incoming data is present.
        if target is not None and updatedData is not None and collectionName is not None:
            
            # Then find the record(s) we need to update.
            targetRecords = None
            try:
                collection = self.database[collectionName]
                # This should put a cursor into targetRecords that contains the matches to iterate through, if any
                targetRecords = collection.find(target)
                
            except errors.OperationFailure as operationFailure:
                print(f"Operation failure while locating records: {operationFailure}")
            except Exception as exception:
                print(f"An unexpected exception occurred while locating records: {exception}") 
            
            # Now that we have the record(s), we want to try to update accordingly.
            # I'm under the belief that proper try-catch structure regarding databases means that
            # you should have each database operation in a separate try-catch block.
            try:
                # Iterate through the matches and update accordingly.
                if targetRecords.count() > 0:
                    updateResult = collection.update_many(target, {"$set": updatedData})
                    
                    # If the update is successful, explicitly confirm that.
                    if updateResult.acknowledged:
                        print(f"{updateResult.modified_count} record(s) updated.")
                        # Return -> The number of objects modified in the collection.
                        return updateResult.modified_count
                    # If the update was unsuccessful, indicate explicitly.
                    else:
                        print("Update failed; server did not acknowledge update request.")
                        return 0
                else:
                    print("No matching records found.")
                    return 0
                
            except errors.OperationFailure as operationFailure:
                print(f"Operation failure during update: {operationFailure}")
            except Exception as exception:
                print(f"An unexpected exception occurred during update: {exception}")
        else:
            raise Exception("No entry can be updated due to the data parameter being empty or no collection being specified.")
            return 0

# Create method to implement the D in CRUD.
    def delete(self, collectionName, target):
        # First, validate that the 'target' is present.
        if target is not None and collectionName is not None:
            # Then confirm that 'target' is in the database.
            collection = self.database[collectionName]
            targetExists = collection.find_one(target)
            
            # If 'target' is in the database, purge it.
            if targetExists:
                deleteResult = collection.delete_one(target)
                if deleteResult.acknowledged:
                    print(f"{deleteResult.deleted_count} record(s) deleted successfully.")
                    # Return -> The number of objects removed from the collection.
                    return deleteResult.deleted_count
                else: 
                    print("Deletion failed; server did not acknowledge delete request.")
                    return 0
            # Otherwise, indicate explicitly.
            else:
                print("Target record not found.")
                return 0                
        else:
            raise Exception("No entry can be deleted due to the data parameter being empty or no collection being specified.")
            return 0