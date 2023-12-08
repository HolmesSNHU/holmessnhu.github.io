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

from CS499_Security import SecurityLayer

def main():
    securityLayer = SecurityLayer()
    securityLayer.RunTests()

if __name__ == "__main__":
    main()
