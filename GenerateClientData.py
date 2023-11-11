import pandas as pd
import random
import string

# A quick script to generate the data we need for the project within certain criteria.
# This script will generate fake client data, which will later be used as part of the account generation process.

# First, we'll generate client names.
# I've sourced 500 of the most common first names in the United States as of 2022 and the 500 most common surnames in the United States as of the 2010 census.
# Each are stored in names.txt and surnames.txt as a comma-separated list.

# Import the names from those files, starting with first names.
with open("names.txt", 'r') as file:
    firstNames = file.read().split(',')
# Now surnames
with open("surnames.txt", 'r') as file:
    lastNames = file.read().split(',')

# We'll also want to generate SSNs but to make it clear that they aren't real, I'll generate them in the format ABC-12-3456.
# To ensure they're unique, we'll have the function accept the used SSNs as an argument and compare against that, regenerating if there's a match.
def generate_ssn(used_SSNs):
    # Keep going until we get a unique combination. A while-true loop is risky sure, but we won't be generating enough SSNs for it to matter.
    while True:
        # Randomly choose letters for the first three characters and numbers for the remaining 6, then merge the two into a candidate SSN
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        numbers = ''.join(random.choices(string.digits, k=6))
        
        candidateSSN = ''.join(letters + numbers)
        
        # If the candidate SSN is not already being used, it's good.
        if candidateSSN not in used_SSNs:
            # Add it to the list of used SSNs
            used_SSNs.add(candidateSSN)
            # Send it back to the requesting generator.
            return candidateSSN
        # If the candidate SSN is already being used, start over.

# A blank set to track the used SSNs
used_SSNs = set()

# Now we can generate the data.
clientsToGenerate = 140
client_data = {
    'first_name': random.choices(firstNames, k=clientsToGenerate),   # Choose a first name at random.
    'last_name': random.choices(lastNames, k=clientsToGenerate), # Choose a last name at random.
    'date_of_birth': pd.date_range(start='1943-01-01', end='2005-01-01', periods=clientsToGenerate).strftime('%Y-%m-%d'), # Choose a date of birth at random. This generates age ranging from 18 to 80
    'SSN': [generate_ssn(used_SSNs) for _ in range(clientsToGenerate)], # Generate a unique, pseudo-random SSN-like character sequence.
    'last_review_date': pd.date_range(start='2022-06-27', end='2023-11-12', periods=clientsToGenerate).strftime('%Y-%m-%d') # Choose a random review date within the last 500 days.
}

# Now we want to spit the generated information out into .csv files for database import.
clientDataFrame = pd.DataFrame(client_data)
clientDataFrame.to_csv('client_data.csv', index=False)
