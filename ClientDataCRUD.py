# **************************************************
# 
# Filename: ClientDataCRUD.py
# Version: 1.0.0
# Purpose: Provide a Python/PyMongo-based interface layer to allow the ClientDataDashboard to interact with data within the MongoDB database.
# 
# Original Version Written: September/October 2023
# Current Version Written: November 2023
# Programmer: Jason Holmes
# Contact Information: jason.holmes3@snhu.edu
# 
# Current Known Issues:
# This CRUD layer was adopted wholesale from a previous project and has some outdated paradigms.
# 
# **************************************************

#!/usr/bin/env python
# coding: utf-8

# PyMongo
from pymongo import MongoClient
from pymongo import errors

# General utility imports
from bson.objectid import ObjectId      # Necessary to strip the ObjectID from the MongoDB data before JSON serialization.
import configparser                     # For parsing the configuration file

# SecurityLayer
from CS499_Security import SecurityLayer

class ClientDataCRUD(object):
    
    """ CRUD operations for CS499_client_database in MongoDB """

    #########################
    # Initialization
    #########################

    def __init__(self, securityLayer, session, username, password):
        
        # Set up a reference for the security layer and token so that the dashboard can establish a single security layer instance.
        self.SL = securityLayer
        self.SESSION = session
        self.TOKEN = session["token"]
        print(f"Session details: {self.SESSION} -- {self.TOKEN}")
        
        # Load the configuration details into a ConfigParser
        self.config = self.LoadConfig("./config/CS499_secure.ini")
        
        # If loading the configuration details failed, we can't continue.
        if (self.config is None):
            print("Failed to load configuration file. Closing the CRUD layer.")
            return
                    
        # Establish a connection to the database using the credentials provided and server details from the configuration file.
        self.database = self.ConnectToDatabase(self.config, username, password)
        
        # If connecting to the database failed, we can't continue.
        if (self.database is None):
            print("Failed to connect the the database. Closing the CRUD layer.")
            return
            
        print("Initialization complete.")

    #######################################################################################################################################

    #########################
    # Database Connectivity
    #########################

    # Loads the login credentials from the configFile.
    # This primarily occurs during initialization but it is separated into its own function for maintainability and encapsulation.
    # It is also for making it easy to create a process to refresh the application's connection to the database with potentially new credentials later. 
    # <IMPROVEMENT> Separate out into a Connection module and generalize for re-use here and in the other modules.
    def LoadConfig(self, configFile):
        
        # Initialize ConfigParser to pull the MongoDB credentials from the configuration file.
        # Keeping the credentials in a server-side configuration file protects them and makes it easier to update them.
        config = configparser.ConfigParser()
        
        # Load the configuration file.
        # As with any external file, it's good practice to contain it in a try-except block.
        try:
            config.read(configFile)
        except FileNotFoundError:                   # Thrown if it can't find the config file
            print("Configuration file not found. Cannot load CRUD layer database credentials.")
            return None
        except configparser.ParsingError as e:      # Thrown if there's some other kind of parsing error.
            print(f"Error parsing the configuration file: {e}")
            return None
        except Exception as e:                      # Catch-all
            print(f"An unexpected exception occurred while loading the configuration file: {e}")
            return None
        return config
        
    # Similar to the LoadConfig function, this is primarily used during initialization but has been separated out for maintainability and encapsulation.
    # This function returns a MongoClient that connects to the server and can be used for the rest of the class.
    # <IMPROVEMENT> Separate out into a Connection module and generalize for re-use here and in the other modules.
    def ConnectToDatabase(self, config, username, password):
        
        # Username and Password should only be passed in this manner if they are login verified.
        # Database details are pulled from the config file.
        # While it's no longer an external file, try-except is still good practice for the likely scenarios.
        try:
            USER = username
            PASS = password
            HOST = config.get("Server", "HOST")
            PORT = config.getint("Server", "PORT")
            DB = config.get("Server", "DB")
            
        except configparser.NoSectionError:     # Thrown if 'CRUDLogin' or 'Server' are not sections within the config file.
            print("Unable to connect to the database. One of the specified sections does not exist in the configuration file.")
            return None
        except configparser.NoOptionError:      # Thrown if 'USER', 'HOST', etc. are not keys within the config file.
            print("Unable to connect to the database. One of the specified keys does not exist in the configuration file.")
            return None
        
        # Connect to MongoDB using those credentials.
        try:
            database = MongoClient('mongodb://%s:%s@%s:%d/%s' % (USER,PASS,HOST,PORT,DB))[DB]
            
            # Verify success, then return the database for use.
            if database is not None:
                print(f"Connected to database: {DB}, type {type(database)}")
                return database
            else:
                print(f"Failed to connected to the {DB} database.")
                return None
            
        except errors.ConnectionFailure as e:     # Thrown if there is some kind of connection error.
            print(f"Failed to connect to MongoDB: {e}")
            return None
        except Exception as e:          # Catch-all.
            print(f"An unexpected exception occurred while connecting to the database: {e}")
            return None

    #######################################################################################################################################

    #########################
    # CRUD Layer
    #########################

    # Complete this create method to implement the C in CRUD.
    def create(self, collectionName, data):
        # First, validate that the 'data' is present and 'collection' has been designated
        if data is not None and collectionName is not None:
            
            # Then attempt to insert it into the database.
            # First, verify the token is valid.
            try:
                collection = self.database[collectionName]
                # print(f"Attempting to access the collection: {collection}")
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
                print(f"Operation failure during create: {operationFailure}")
            except Exception as exception:
                print(f"An unexpected exception occurred during creation: {exception}")
        else:
            raise Exception("Nothing to save because data parameter is empty.")
            return False

    # Create method to implement the R in CRUD.
    def read(self, collectionName, data):
        # First, validate that the 'data' is present.
        if data is not None and collectionName is not None:
            # Then attempt to read the requested data from the database.
            try:
                collection = self.database[collectionName]
                # print(f"Attempting to access collection: {collection}")
                # This should return a list that either contains the results or is empty
                results = [entry for entry in collection.find(data)]
                return results
            
            except errors.OperationFailure as operationFailure:
                print(f"Operation failure during read: {operationFailure} in {type(self.database[collectionName])}")
                # If the return fails, we want to gracefully handle it by ensuring the empty list returns.
                return []
            except Exception as exception:
                print(f"An unexpected exception occurred during read: {exception}") 
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
            try:
                collection = self.database[collectionName]
                targetExists = collection.find_one(target)

            except errors.OperationFailure as operationFailure:
                print(f"Operation failure while locating records: {operationFailure}")
            except Exception as exception:
                print(f"An unexpected exception occurred while locating records: {exception}")             
                
            # If 'target' is in the database, purge it.
            try:
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
                    
            except errors.OperationFailure as operationFailure:
                print(f"Operation failure during update: {operationFailure}")
            except Exception as exception:
                print(f"An unexpected exception occurred during deletion: {exception}")
        else:
            raise Exception("No entry can be deleted due to the data parameter being empty or no collection being specified.")
            return 0
    
    # Function to update the security token for the CRUD layer instance.
    # Used for refreshing security tokens for existing users, if needed.
    def UpdateToken(self, token):
        if token is not None:
            self.TOKEN = token
    