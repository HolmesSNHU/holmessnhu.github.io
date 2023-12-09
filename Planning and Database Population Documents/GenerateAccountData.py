# **************************************************
# 
# Filename: GenerateAccountData.py
# Version: 1.0.0
# Purpose: Generate the account data for populating a database with fake-but-realistic financial data.
# 
# Written: November 2023
# Programmer: Jason Holmes
# Contact Information: jason.holmes3@snhu.edu
# 
# Current Known Issues:
# 
# **************************************************

import pandas as pd
import random

# Another quick script, this time to generate the account data we'll need.
# We'll want to base some of this information on the clients themselves, so the client data
# has been generated first, put through the database, then exported again. We'll import that now.

client_data = pd.read_csv('clients_export.csv')

# Because of the way we're incorporating client IDs, we'll structure it differently this time.
# And that means a function to generate the account data and attaches it to a specific client.
def generate_account_data(client_data):
    
    # Designate the number of accounts to generate
    num_accounts = 400
    # Limit the number of accounts per client. Probably not necessary, but we'll do it anyway.
    max_accounts_per_client = 4
    # A dictionary for the clients to keep track of the number of accounts each client has had generated.
    num_accounts_dict = {client_id: 0 for client_id in client_data['_id']}

    # We'll want to limit the number of retirement accounts to more accurately reflect a given book of business.
    retirement_percentage = 0.4     # 40% is about right based on my experience.

    # Create an empty container for the account data
    account_data = []

    # And now it's finally time to generate the accounts. For each num_accounts:
    for i in range(num_accounts):
        # We'll maintain a list of eligible clients to ensure they don't go over 4 accounts.
        eligible_clients = [client_id for client_id, num_accounts in num_accounts_dict.items() if num_accounts < max_accounts_per_client or num_accounts == 0]
        
        # We'll stop if there are no more eligible clients
        if not eligible_clients:
            break

        # Otherwise, choose a random client from the eligible options and increment their account counter
        client_id = random.choice(eligible_clients)
        num_accounts_dict[client_id] += 1

        # Choose whether the account will be retirement or non-retirement.
        is_retirement = random.choices([True, False], weights=[retirement_percentage, 1 - retirement_percentage], k=1)[0]
        account_class = 'retirement' if is_retirement else 'non-retirement'
        
        # Decide on the account type within common Retirement or Non-Retirement account types.
        account_types = ['Rollover IRA', 'Traditional IRA', 'SEP IRA'] if is_retirement else ['Trust Account', 'TOD Account', 'Individual Account']
        # Generate the nickname by taking the client's first name and adding one of the appropriate account types at random.
        account_nickname = f"{client_data.loc[client_data['_id'] == client_id, 'first_name'].iloc[0]}'s {random.choice(account_types)}"
        # Generate account value details like total value, current liquid cash, and year-to-date distributions.
        # The parameters of these are pulled from my experience in the field and typical values therein.
        account_value = round(random.uniform(200000, 2000000), 2)
        cash_available_percentage = random.uniform(0.1, 0.15 # You want to keep some cash but never too much, since liquid cash isn't doing any work.
        cash_available = round(account_value * cash_available_percentage, 2)
        ytd_distributions = round(random.uniform(0, 100000), -2) if random.random() < 0.2 else 0 # Most clients don't take distributions.
        # Also generate a required minimum distribution amount if it's a retirement account and the client is over 73 years old (current RMD age)
        rmd_amount = round(account_value * random.uniform(0.03, 0.05), 2) if is_retirement and client_data.loc[client_data['_id'] == client_id, 'date_of_birth'].iloc[0] <= '1950-11-12' else 0

        # Add the generated account to the list.
        account_data.append({
            '_id': client_id,
            'account_nickname': account_nickname,
            'account_class': account_class,
            'account_value': account_value,
            'cash_available': cash_available,
            'ytd_distributions': ytd_distributions,
            'rmd_amount': rmd_amount
        })

    return account_data

# With the function defined, we can actually use it! Once generated, we spit it out to a .csv same as last time.
accounts_data = generate_account_data(client_data)
accountsDataFrame = pd.DataFrame(accounts_data)
accountsDataFrame.to_csv('account_data.csv', index=False)