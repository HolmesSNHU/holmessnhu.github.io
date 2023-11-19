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
import uuid         # For generating unique user IDs (UUIDs)

class SecurityLayer:
    def __init__ (self):
        
        # Store some default values for login and session management.
        self.loginFailureThreshold = 5      # Number of failed login attempts before account is locked
        self.sessionLifespan = 600          # Lifespan of session in seconds since last activity. Also used for account lockouts.
        self.tokenSize = 32                 # Number of bytes that a security token should contain. 32 should be adequate for our purposes.
                
        # Store active user sessions in a local dictionary.
        # <IMPROVEMENT>: A more robust database-centric solution would improve scaling and usability.
        self.activeSessions = {}
        
        # Load the configuration details into a ConfigParser
        self.config = self.LoadConfig("./database/CS499_secure.ini")
        
        # If loading the configuration details failed, we can't continue.
        if (self.config is None):
            print("Failed to load configuration file. Closing the security layer.")
            return
            
        # Establish a connection to the database using the credentials from the configuration file.
        self.database = self.ConnectToDatabase(self.config)
        
        # If connecting to the database failed, we can't continue.
        if (self.database is None):
            print("Failed to connect the the database. Closing the security layer.")
            return
        
        # Establish a collection shortcut for later use
        collectionName = self.config.get("ClientDB", "COL")
        try:
            self.collection = self.database[collectionName]
            
            # Verify the connection was successful.
            if self.collection is not None:
                print(f"Connected to collection: {collectionName}, data type {type(self.collection)}")
            else:
                print(f"Failed to connect to the {collectionName} collection.")
                return
            
            # Establish a collection shortcut for later use.
        
        except errors.ConnectionFailure as e:     # Thrown for connection errors
            print(f"Connection error: {e}")
            return
        except Exception as e:                  # Catch-all
            print(f"An unexpected exception occurred while connecting to the collection: {e}")
            return
                
    # EXTREMELY BASIC, temporary unit tests for functionality testing.
    def RunTests(self):
    
        print("Running tests.")
        print("Test 0: Adding test user...")
        # Temporary testing variables.
        self.tempUsername = "admin"
        self.tempPassword = "root"
        self.AddTestUser(self.tempUsername, self.tempPassword)
        
        print("Test 1: Testing user verification...")
        verifiedUser = self.VerifyUser(self.tempUsername)
        if verifiedUser:
            print(f"Verification passed for {self.tempUsername}")
        else:
            print(f"Verification failed for {self.tempUsername}")
        
        print("Test 2: Testing password hashing...")
        hashedPassword = self.HashPassword(self.tempPassword)
        if self.VerifyPassword(hashedPassword, verifiedUser.get("hashed_password")):
            print(f"Hashed password verification passed for {self.tempUsername}")
        else:
            print(f"Hashed password verification failed for {self.tempUsername}")
            
        print("Test 3: Testing authentication...")
        authenticated = self.AuthenticateUser(self.tempUsername, self.tempPassword)
        if authenticated:
            print(f"Authentication passed for {self.tempUsername}")
        else:
            print(f"Authentication failed for {self.tempUsername}")
            
        print("Test 4: Testing session generation...")
        session = self.LoginSuccess(self.tempUsername)
        if session:
            print(f"Session generation passed for {self.tempUsername}")
            print(f"Session details: UUID: '{session['UUID']}', token: '{session['token']}'")
        else:
            print(f"Session generation failed for {self.tempUsername}")
            
        print("Test 5: Testing session validation...")
        sessionValidated = self.ValidateSession(session["UUID"], session["token"])
        if sessionValidated:
            print(f"Session Authentication passed for {self.tempUsername}")
        else:
            print(f"Session Authentication failed for {self.tempUsername}")
            
        print("Test 6: Testing account lock...")
        self.AccountLock(self.tempUsername, True)
        verifiedUser = self.VerifyUser(self.tempUsername)
        locked = self.GetAccountLocked(verifiedUser)
        if locked:
            print(f"Account locking passed for {self.tempUsername}")
        else:
            print(f"Account locking failed for {self.tempUsername}")
            
        print("Test 7: Testing account unlock...")
        self.AccountLock(self.tempUsername, False)
        verifiedUser = self.VerifyUser(self.tempUsername)
        locked = self.GetAccountLocked(verifiedUser)
        if not locked:
            print(f"Account unlocking passed for {self.tempUsername}")
        else:
            print(f"Account unlocking failed for {self.tempUsername}")
    
    # TEMPORARY FUNCTION FOR TESTING ONLY
    def AddTestUser(self, username, password):
        userExists = self.VerifyUser(username)
        if (userExists):
            print(f"Test user {username} already exists. No need to add again. Skipping.")
            return
            
        hashed_password = self.HashPassword(password)
        
        if hashed_password:
            tempUser = {
                "username": username,
                "hashed_password": hashed_password,
                "role": "readWrite",
                "isLocked": False,
                "lastLoginAttempt": datetime.datetime.now(),
                "recentFailedAttempts": 0
            }
            
            try:
                self.collection.insert_one(tempUser)
                print(f"User '{username}' added successfully.")
            except Exception as e:
                print(f"Failed to add user '{username}' during AddTestUser: {e}")
        else:
            print(f"Failed to hash password for user '{username}'")
    
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
    def ConnectToDatabase(self, config):
        
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
            

    
    # Function to authenticate a login attempt by verifying the provided credentials against the credentials stored in the database.
    # Just provides a boolean authentication and the dashboard should call success or failure accordingly for session management purposes.
    def AuthenticateUser(self, username, password):
        
        # Verify user exists.
        user = self.VerifyUser(username)
        
        # If they don't exist, reject the login attempt.
        # Cannot trigger a LoginFailure() for the user since the user does not exist.
        # <IMPROVEMENT> Expand the user session to include pre-login periods so that each IP address only has so many login attempts before they are locked out.
        # <IMPROVEMENT> Communicate to the dashboard the reason why the login failed so the user can decide how to proceed.
        if user is None:
            print(f"Login attempt for {username} failed. No matching user.")
            return False
        
        # Before we test the login credentials, check the account's locked status.
        # <IMPROVEMENT> Communicate to the dashboard the reason why the login failed so the user can decide how to proceed.
        if self.GetAccountLocked(user):
            print(f"Login attempt for {username} failed; account is locked.")
            return False
        
        # Hash the supplied password using SHA-256
        hashedPassword = self.HashPassword(password)
        
        # Retrieve the stored password hash from user data
        storedPasswordHash = user.get("hashed_password")
        
        # Verify hashed credentials against each other.
        # This will return a simple boolean result, so we can just return it directly.
        # <IMPROVEMENT> Communicate to the dashboard the reason why the login failed (if it did) so the user can decide how to proceed.
        return self.VerifyPassword(hashedPassword, storedPasswordHash)
        
    
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
        
        # Secrets provides a secure comparison function to protect the intrinsic information about the passwords.
        # This function takes two hashes and returns a boolean based on their comparison, so we can pass that straight on.
        match = secrets.compare_digest(inputPasswordHash, storedPasswordHash)
        return match
        
        
    # Function for handling successful login attempts. Called by the dashboard after a successful AuthenticateUser
    # Returns a security token.
    def LoginSuccess(self, username):
        
        # A successful authentication requires that the user and their credentials have been verified, so we can skip straight to functionality.
                
        # Firstly, a successful login attempt should clear the recent failures.
        # We'll update the last login attempt at the same time just for completeness's sake.
        self.UpdateDatabase(username, { 
                    "recentFailedAttempts" : 0,
                    "lastLoginAttempt": datetime.datetime.now()
                })
        
        # Second, generate an active session for the user and return it.
        return self.GenerateActiveSession(username)
    
    # Function to handle account locking and unlocking.
    # Accepts a database document of the user's information.
    # Returns a boolean for whether the account is currently locked after processing is complete.
    def GetAccountLocked(self, user):
        
        # First, check to see if the user is currently locked. If it isn't, we can carry on as normal.
        accountLocked = user.get("isLocked")
        if not accountLocked:
            return False
            
        # Store the username for future use.
        username = user.get("username")
        
        # Since the account is locked, first check to see when the last login attempt took place. If it's beyond the lockout duration, we can unlock it.
        lastLoginAttempt = user.get("lastLoginAttempt")
        # Subtracting two datetime objects results in a timedelta object, which lets us pull total_seconds() directly.
        if (datetime.datetime.now() - lastLoginAttempt).total_seconds() > self.sessionLifespan:
            # If it's been longer than the session lifespan, unlock the account and return that there is no lock.
            self.AccountLock(username, False)
            return False
        else:
            # Otherwise, it's locked and this is a failed login attempt.
            return True
    
    # Function for handling failed login attempts. Called by the dashboard after a failed AuthenticateUser
    def LoginFailed(self, username):
        
        # There are situations where a login can fail but not be attributed to any specific user.
        # Retrieve the user information.
        user = self.VerifyUser(username)
        
        # if the user doesn't exist, we're done.
        # <IMPROVEMENT> Expand the user session to include pre-login periods so that each IP address only has so many login attempts before they are locked out.
        if user is None:
            return
        
        # Otherwise, the user exists so we can use their data.
        recentFailedAttempts = user.get("recentFailedAttempts", 0) + 1
        
        # A failed login attempt should increment the recent failed attempts and last login attempt time.
        self.UpdateDatabase(username, { 
                        "recentFailedAttempts" : recentFailedAttempts,
                        "lastLoginAttempt": datetime.datetime.now()
                    })
        
        # Check against threshold
        if recentFailedAttempts >= self.loginFailureThreshold:
            # Lock if threshold exceeded
            self.AccountLock(username, True)
        
    # Function to handle locking accounts after several failed login attempts and unlocking as needed.
    def AccountLock(self, username, lockStatus):
        # We've done the necessary verification before this ever gets called.
        self.UpdateDatabase(username, { "isLocked": lockStatus })
    
    # Function to manage generating an active session.
    # An active session includes a unique user_ID for the session, the attached username, the lastActivity timestamp, and the generated security token.
    # It is only called when a login is successful and should return the security token for delivery to the client.
    def GenerateActiveSession(self, username):
        # An active session as three things; the username, the lastActivity timestamp, and the security token.
        # We have the first one, so we need to generate the last two.
        
        # Generate an initial lastActivity timestamp.
        lastActivity = datetime.datetime.now()
        
        # Generate a security token.
        securityToken = self.GenerateSecurityToken()
        
        # Generate a UUID for the session
        sessionID = self.GenerateUUID()
        
        # The security layer stores all active sessions in self.activeSessions for verification purposes.
        # <IMPROVEMENT>: A more robust database-centric solution would improve scaling and usability.        
        sessionData = {
            "username": username,
            "token": securityToken,
            "lastActive": lastActivity
        }
        self.activeSessions[sessionID] = sessionData
        
        # Finally, return the relevant session details for transmission to the user and local storage.
        return {"UUID": sessionID, "token": securityToken}
    
    # Function to generate a unique user ID for each session. It's just a numeric ID so it should mesh well for data structure and database purposes.
    def GenerateUUID(self):
        # Python's UUID4 function doesn't technically GUARANTEE uniqueness but it's so astronomically unlikely that it may as well be unique.
        # Converting it to a string before returning it ensures that it's easily stored and handled.
        return str(uuid.uuid4())
    
    # Function to generate and return a security token, which will be bundled into the active session
    def GenerateSecurityToken(self):
        # A security token just needs to be something that's sufficiently difficult to guess which can be shared between client and server securely for verification.
        # We'll use the Python secrets library to generate the security token as a random string of characters.
        # urlsafe takes a number of bytes to use to generate a token that is safe for usage in a URL. that should be enough for our purposes
        return secrets.token_urlsafe(self.tokenSize)
    
    # Function to validate the user's current session. Called every time a request is made.
    def ValidateSession(self, UUID, token):
        
        # The dictionary isn't technically external but we can still try-except it.
        
        try:
            # Confirm the UUID is present. If it isn't, reject validation.
            if UUID not in self.activeSessions:
                return False
            
            # The session exists at this point. Get a reference to the session and current time since we'll be using both a few times.
            session = self.activeSessions[UUID]
            currentTime = datetime.datetime.now()
            
            # Confirm the UUID has not yet expired. If it has, end the session and reject validation.
            if (currentTime - session["lastActive"]).total_seconds() > self.sessionLifespan:
                self.EndActiveSession(UUID)
                return False
                
            # Confirm the security token matches. If it doesn't, end the session and reject validation.
            if token != session["token"]:
                self.EndActiveSession(UUID)
                return False
                
            # We only reach this point if the session exists and is currently valid.
            
            # Update the session's last active time and confirm validity.
            session["lastActive"] = currentTime
            return True
            
        except KeyError as e:           # Thrown if the key requested 'lastActive', 'token' are not present. Should never happen. Should.
            print(f"Error in session validation. {e}")
            return False
        except Exception as e:          # Catch-all
            print(f"An unexpected exception occurred during session validation: {e}")
            return False
            
        
    
    # Function to end an active session. Called only when validation identifies an expired session.
    def EndActiveSession(self, UUID):
        # Technically it's not necessary to verify the UUID is in the dictionary since we only get here if it is, but it won't hurt anything either.
        if UUID in self.activeSessions:
            # activeSessions is a dictionary of dictionaries, so we need to purge the session dictionary and THEN purge the activeSessions entry.
            self.activeSessions[UUID].clear()       # Clears out all elements of the dictionary contained at self.activeSessions[UUID]
            del self.activeSessions[UUID]           # Deletes the UUID entry in self.activeSessions.
            
        return
        
    # Function to update database values for a given user. Only called after verification is completed.
    # Accepts the target username and a dictionary of {field : newValue}. Returns boolean for success or failure.
    def UpdateDatabase(self, username, dataDict):
        
        # This function is mostly for ease of error-handling. I made it a bit generic so I can use it anywhere I need to.
        # <IMPROVEMENT> Add in dataDict verification to ensure data being set matches database expectations.
        
        try:
            self.collection.update_one({"username": username}, { "$set": dataDict })
            return True
        except errors.OperationFailure as e:        # Throws if the operation fails for some reason
            print(f"MongoDB update failed. Username: {username} -- Data: {dataDict} -- Error: {e}")
            return False
        except Exception as e:          # Catch-all
            print(f"An unexpected exception occurred during database update: Username: {username} -- Data: {dataDict} -- Error: {e}")
            return False
        
        # Just in case the try-except block is no good.
        return False
    