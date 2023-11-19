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
        
        # Store some default values for login and session management.
        self.loginFailureThreshold = 5      # Number of failed login attempts before account is locked
        self.sessionLifespan = 600          # Lifespan of session in seconds since last activity. Also used for account lockouts.
        
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
    
    # Function to authenticate a login attempt by verifying the provided credentials against the credentials stored in the database.
    # Just provides a boolean authentication and the dashboard should call success or failure accordingly for session management purposes.
    def AuthenticateUser(self, username, password):
        
        # Verify user exists.
        user = VerifyUser(username)
        
        # If they don't exist, reject the login attempt.
        # Cannot trigger a LoginFailure() for the user since the user does not exist.
        # <IMPROVEMENT> Expand the user session to include pre-login periods so that each IP address only has so many login attempts before they are locked out.
        # <IMPROVEMENT> Communicate to the dashboard the reason why the login failed so the user can decide how to proceed.
        if user is None:
            print(f"Login attempt for {username} failed. No matching user.")
            return False
        
        # Before we test the login credentials, check the account's locked status.
        # <IMPROVEMENT> Communicate to the dashboard the reason why the login failed so the user can decide how to proceed.
        if GetAccountLocked(user):
            print(f"Login attempt for {username} failed; account is locked.")
            return False
            
        
        # Hash the supplied password using SHA-256
        hashedPassword = HashPassword(password)
        
        # Retrieve the stored password hash from user data
        storedPasswordHash = user.get("hashed_password")
        
        # Verify hashed credentials against each other.
        # This will return a simple boolean result, so we can just return it directly.
        # <IMPROVEMENT> Communicate to the dashboard the reason why the login failed (if it did) so the user can decide how to proceed.
        return VerifyPassword(hashedPassword, storedPasswordHash):
        
    
    # Function for verifying that a given user is present in the login database. If so, return the user data for use.
    def VerifyUser(self, username):
        
        # Verify the user exists.
        verifyUser = self.collection.find_one({"username": username})
        if verifyUser:
            # If so, return the user data for use.
            return verifyUser
        else:
            # Otherwise, make a note in the log and move on.
            print("Username not found.")
            return None
    
    # Password hashing function for login attempts and registration
    def HashPassword(self, password):
        
        # We'll use the SHA-256 algorithm from the hashlib library to handle this.
        # <IMPROVEMENT> Implement salting prior to the hashing. Be sure to store the generated salt to the login database and update any existing logins accordingly.
        try:
            hashedPassword = hashlib.sha256(password.encode()).hexdigest()
            
            # Hashlib won't give us an error if the hashing fails so to verify that the hashing was successful, we check for the correct length.
            if len(hashedPassword) != 64:
                print("Password hashing failed.")
                return None
            else:
                return hashedPassword
            
        except Exception as e:
            print(f"Hashing error: {e}")
            return None
    
    # Function to verify password hashes match using hashlib.
    def VerifyPassword(self, inputPasswordHash, storedPasswordHash):
        
        # Hashlib provides a secure comparison function to protect the intrinsic information about the passwords.
        # This function takes two hashes and returns a boolean based on their comparison, so we can pass that straight on.
        match = hashlib.compare_digest(inputPasswordHash, storedPasswordHash)
        return match
        
        
    # Function for handling successful login attempts. Called by the dashboard after a successful AuthenticateUser
    # Returns a security token.
    def LoginSuccess(username):
        
        # A successful authentication requires that the user and their credentials have been verified, so we can skip straight to functionality.
                
        # Firstly, a successful login attempt should clear the recent failures.
        # We'll update the last login attempt at the same time just for completeness's sake.
        # <IMPROVEMENT> Move all update fields to a DatabaseUpdate(username, {field, value}) function.
        self.collection.update_one("username": username, {
            "$set": { "recentFailedAttempts" : 0,
                      "lastLoginAttempt": datetime.now()
            }
        })
        
        # Second, generate a security token and return it.
        return GenerateSecurityToken()
    
    def GenerateSecurityToken():
    
    # Function to handle account locking and unlocking.
    # Accepts a database document of the user's information.
    # Returns a boolean for whether the account is currently locked after processing is complete.
    def GetAccountLocked(user):
        
        # First, check to see if the user is currently locked. If it isn't, we can carry on as normal.
        accountLocked = user.get("isLocked")
        if accountLocked is False:
            return False
            
        # Store the username for future use.
        username = user.get("username")
        
        # Since the account is locked, first check to see when the last login attempt took place. If it's beyond the lockout duration, we can unlock it.
        lastLoginAttempt = user.get("lastLoginAttempt")
        # Subtracting two datetime objects results in a timedelta object, which lets us pull total_seconds() directly.
        if (datetime.now() - lastLoginAttempt).total_seconds() > self.sessionLifespan:
            # If it's been longer than the session lifespan, unlock the account and return that there is no lock.
            AccountLock(username, False)
            return False
        else:
            # Otherwise, it's locked and this is a failed login attempt.
            return True
    
    # Function for handling failed login attempts. Called by the dashboard after a failed AuthenticateUser
    def LoginFailed(username):
        
        # There are situations where a login can fail but not be attributed to any specific user.
        # Retrieve the user information.
        user = VerifyUser(username)
        
        # if the user doesn't exist, we're done.
        # <IMPROVEMENT> Expand the user session to include pre-login periods so that each IP address only has so many login attempts before they are locked out.
        if user is None:
            return
        
        # Otherwise, the user exists so we can use their data.
        recentFailedAttempts = user.get("recentFailedAttempts", 0) + 1
        
        # A failed login attempt should increment the recent failed attempts and last login attempt time.
        # <IMPROVEMENT> Move all update fields to a DatabaseUpdate(username, {field, value}) function.
        self.collection.update_one("username": username, {
            "$set": { "recentFailedAttempts" : recentFailedAttempts,
                      "lastLoginAttempt": datetime.now()
            }
        })
        
        # Check against threshold
        if recentFailedAttempts >= self.loginFailureThreshold:
            # Lock if threshold exceeded
            AccountLock(username, True)
        
    # Function to handle locking accounts after several failed login attempts and unlocking as needed.
    def AccountLock(username, lockStatus):
        # We've done the necessary verification before this ever gets called.
        # <IMPROVEMENT> Move all update fields to a DatabaseUpdate(username, {field, value}) function.
        self.collection.update_one("username": username, {
            "$set": { "isLocked": lockStatus }
        })
    
    # Upon user request, validate the session
        # Make sure the session is present
        # Make sure the session hasn't expired
        # Update session's last active so that future checks use the most recent activity to compare against
    
    # 
    