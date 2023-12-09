# **************************************************
# 
# Filename: SecurityTestDriver.py
# Version: 1.0.0
# Purpose: Basic driver to run the security layer's temporary built-in unit tests to validate functionality.
# 
# Written: November 2023
# Programmer: Jason Holmes
# Contact Information: jason.holmes3@snhu.edu
# 
# Current Known Issues:
# 
# **************************************************

from ClientDataSecurity import SecurityLayer

def main():
    # Initialize the security layer.
    securityLayer = SecurityLayer()
    
    # Run a series of simple unit tests for functionality testing.
        
    print("Running tests.")
    print("Test 0: Adding test user...")
    # Temporary testing variables.
    self.tempUsername = "admin"
    self.tempPassword = "root"
    securityLayer.AddTestUser(self.tempUsername, self.tempPassword)
    
    print("Test 1: Testing user verification...")
    verifiedUser = securityLayer.VerifyUser(self.tempUsername)
    if verifiedUser:
        print(f"Verification passed for {self.tempUsername}")
    else:
        print(f"Verification failed for {self.tempUsername}")
    
    print("Test 2: Testing password hashing...")
    hashedPassword = securityLayer.HashPassword(self.tempPassword)
    if securityLayer.VerifyPassword(hashedPassword, verifiedUser.get("hashed_password")):
        print(f"Hashed password verification passed for {self.tempUsername}")
    else:
        print(f"Hashed password verification failed for {self.tempUsername}")
        
    print("Test 3: Testing authentication...")
    authenticated = securityLayer.AuthenticateUser(self.tempUsername, self.tempPassword)
    if authenticated:
        print(f"Authentication passed for {self.tempUsername}")
    else:
        print(f"Authentication failed for {self.tempUsername}")
        
    print("Test 4: Testing session generation...")
    session = securityLayer.LoginSuccess(self.tempUsername)
    if session:
        print(f"Session generation passed for {self.tempUsername}")
        print(f"Session details: UUID: '{session['UUID']}', token: '{session['token']}'")
    else:
        print(f"Session generation failed for {self.tempUsername}")
        
    print("Test 5: Testing session validation...")
    sessionValidated = securityLayer.ValidateSession(session["UUID"], session["token"])
    if sessionValidated:
        print(f"Session Authentication passed for {self.tempUsername}")
    else:
        print(f"Session Authentication failed for {self.tempUsername}")
        
    print("Test 6: Testing account lock...")
    securityLayer.AccountLock(self.tempUsername, True)
    verifiedUser = securityLayer.VerifyUser(self.tempUsername)
    locked = securityLayer.GetAccountLocked(verifiedUser)
    if locked:
        print(f"Account locking passed for {self.tempUsername}")
    else:
        print(f"Account locking failed for {self.tempUsername}")
        
    print("Test 7: Testing account unlock...")
    securityLayer.AccountLock(self.tempUsername, False)
    verifiedUser = securityLayer.VerifyUser(self.tempUsername)
    locked = securityLayer.GetAccountLocked(verifiedUser)
    if not locked:
        print(f"Account unlocking passed for {self.tempUsername}")
    else:
        print(f"Account unlocking failed for {self.tempUsername}")

if __name__ == "__main__":
    main()
