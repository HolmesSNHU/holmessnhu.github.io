# **************************************************
# 
# Filename: CS499_Security.py
# Version: 1.0.0
# Purpose: Provide a Python-based security layer to allow the ClientDataDashboard to securely log into its database and manage the user"s session.
# 
# Written: November 2023
# Programmer: Jason Holmes
# Contact Information: jason.holmes3@snhu.edu
# 
# Current Known Issues:
# * This is a limited-scope foundation. Obvious potential improvements marked by <IMPROVEMENT> comments.
# 
# **************************************************

# PyMongo
from pymongo import MongoClient
from pymongo import errors

# General utility imports
import hashlib      # For password hashing
import secrets      # For token generation
import datetime     # For timestamp generation
import configparser # For parsing the configuration file

class SecurityLayer:
    def __init__ (self):
          
        # Store active user sessions in a local dictionary.
        # <IMPROVEMENT>: A more robust database-centric solution would improve scaling and usability.
        self.activeSessions = {}
        
        # Load the configuration details into a ConfigParser
        self.config = LoadConfig("./database/CS499_secure.ini")
        
        # If loading the configuration details failed, we can't continue.
        if (self.config is None):
            print("Failed to load configuration file. Closing the security layer.")
            return
            
        # Establish a connection to the database using the credentials from the configuration file.
        self.database = ConnectToDatabase(self.config)
        
        # If connecting to the database failed, we can't continue.
        if (self.database is None):
            print("Failed to connect the the database. Closing the security layer.")
            return
        
        # Establish a collection shortcut for later use
        COL = config.get("ClientDB", "COL")
        try:
            self.collection = self.database['%s' % (COL)]
            
            # Verify the connection was successful.
            if self.collection is not None:
                print(f"Connected to collection: {COL}")
            else:
                print(f"Failed to connect to the {COL} collection.")
                return
            
            # Establish a collection shortcut for later use.
        
        except errors.ConnectionError as e:     # Thrown for connection errors
            print(f"Connection error: {e}")
            return
        except Exception as e:                  # Catch-all
            print(f"An unexpected exception occurred while connecting to the collection: {e}")
            return
    
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
            print("Configuration file not found. Cannot load database credentials.")
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
    def ConnectToDatabase(self, config)
        
        # Collect credentials and database details from the config file.
        # While it's no longer an external file, try-except is still good practice for the likely scenarios.
        try:
            USER = config.get("ClientDB", "USER")
            PASS = config.get("ClientDB", "PASS")
            HOST = config.get("ClientDB", "HOST")
            PORT = config.getint("ClientDB", "PORT")
            DB = config.get("ClientDB", "DB")
            
        except configparser.NoSectionError:     # Thrown if 'ClientDB' is not a section within the config file.
            print("Unable to connect to the database. One of the specified sections does not exist in the configuration file.")
            return None
        except configparser.NoOptionError:      # Thrown if 'USER', 'HOST', etc. are not keys within the config file.
            print("Unable to connect to the database. One of the specified keys does not exist in the configuration file.")
            return None
        
        # Connect to MongoDB using those credentials.
        try:
            database = MongoClient('mongodb://%s:%s@%s:%d/%s' % (USER,PASS,HOST,PORT,DB))
            
        except errors.ConnectionError as e:     # Thrown if there is some kind of connection error.
            print(f"Failed to connect to MongoDB: {e}")
            return None
        except Exception as e:          # Catch-all.
            print(f"An unexpected exception occurred while connecting to the database: {e}")
            return None
            
        # Verify success, then return the database for use.
        if database is not None:
            print(f"Connected to database: {DB}")
            return database
        else:
            print(f"Failed to connected to the {DB} database.")
            return None
            
    # On login attempt:
        # Hash a password
        # Retrieve password hash from database
        # Authenticate a user against the login database
    
    # On login success:
        # Reset failure count
        # Generate a security token
    
    # On login failure:
        # Increment failed attempts
        # Check against threshold
        # Lock if threshold exceeded
        
    # Upon user request, validate the session
        # Make sure the session is present
        # Make sure the session hasn't expired
        # Update session's last active so that future checks use the most recent activity to compare against
    
    # 
    