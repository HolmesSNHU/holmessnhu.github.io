# **************************************************
# 
# Filename: ClientDataDashboard.py
# Version: 1.0.0
# Purpose: Provide a Dash by Plotly-based single page dashboard application for visualizing and interacting with data from the MongoDB database.
# 
# Original Version Adapted: September/October 2023
# Current Version Written: November 2023
# Programmer: Jason Holmes
# Contact Information: jason.holmes3@snhu.edu
# 
# Current Known Issues:
# * This was heavily adapted from a class project in which the original code structure was provided.
# 
# **************************************************

#######################################################################################################################################

###########################
# Module Imports
###########################

# Configure the necessary Python module imports for dashboard components
# Dash by Plotly
from dash import Dash
from dash import dcc, html
from dash import dash_table
from dash.dependencies import Input, Output, State
import dash_leaflet as dl
import plotly.express as px

# Plotting Routines for graphs, charts, etc.
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt

# PyMongo utilities
from pymongo import errors

# General utility imports
import base64                   # Image encoding
from datetime import datetime   # Datetime encoding

# Configure OS routines
import os

# Import CRUD interface layer
from ClientDataCRUD import ClientDataCRUD

# Import Security Layer
from CS499_Security import SecurityLayer

#######################################################################################################################################
#######################################################################################################################################

#########################
# Runtime Setup
# app must be declared before callbacks.

#########################
# Set up the various modules we'll need.
# sl = Integrate the SecurityLayer for verification.

# Whenever initiating contact with external elements, try-catch is a good idea.
try:
    sl = SecurityLayer()
    
except errors.OperationFailure as operationFailure:
    print(f"Operation failure: {operationFailure}")
except Exception as exception:
    print(f"An unexpected exception occurred: {exception}") 

# These will be established once login is verified:
# db = Connect to database via CRUD Module
# df = A DataFrame containing the data from the database
db = None
df = None


# Set up the Dash framework, layout declarations, and state storage.
app = Dash(__name__)

#########################
# Login Layout / View
#########################

loginLayout = html.Div(
    style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'width': '40%',
        'margin': 'auto'
    }, children =[
        html.H1("Login to Access Dashboard"),
        html.Div(
            style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center'
            }, children=[
            html.Div(
                style={
                    'display': 'flex',
                    'alignItems': 'right',
                    'marginBottom': '10px'
                }, children=[
                    html.Label("Username: ", style={'marginRight':'10px', 'width':'100px'}),
                    dcc.Input(id="username-input", type="text", value="", placeholder="Enter your username."),
                ]
            ),
            html.Div(
                style={
                    'display': 'flex',
                    'alignItems': 'right',
                    'marginBottom': '10px'
                }, children=[
                    html.Label("Password: ", style={'marginRight':'10px', 'width':'100px'}),
                    dcc.Input(id="password-input", type="password", value="", placeholder="Enter your password."),
                ]
            ),
            html.Div(id='loginResult', children=[]),
            html.Div([
                html.Button("Login", id="login-button", n_clicks=0, style={'margin-top':'20px', 'margin-right':'10px','alignItems': 'center'}),
                html.Button("Register", id="register-button", n_clicks=0, style={'margin-top':'20px', 'margin-right':'10px','alignItems': 'center'}),
                html.Button("Register (Admin)", id="registerAdmin-button", n_clicks=0, style={'margin-top':'20px','alignItems': 'center'})
                ])
            ]
        )
    ]
)

#########################
# Dashboard Layout / View
#########################

#image_filename = '6 - Grazioso Salvare Logo.png' # replace with your own image
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())

dashboardLayout = html.Div(style={'max-width':'80%', 'margin':'auto'}, children=[
    #html.Div(id='hidden-div', style={'display':'none'}),
    #html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                         #style={'max-width':'200px', 'max-height':'200px'})),
    html.Center(html.B(html.H1('CS-499 Dashboard'))),
    html.Center(html.H3('Written by Jason Holmes')),
    html.Hr(),
    html.Div(
        #FIXME Add in code for the interactive filtering options. For example, Radio buttons, drop down, checkboxes, etc.
        dcc.RadioItems(
            id='filter-type',
            options=[
                {'label': 'Retirement Accounts', 'value':'retirement'},
                {'label': 'Non-Retirement Accounts', 'value':'nonRetirement'},
                {'label': 'RMD Status', 'value':'RMDs'},
                {'label': 'Overdue Reviews', 'value':'reviews'},
                {'label': 'No Filter', 'value':'reset'}
            ],
            value='reset', # Default input
            labelStyle={'display':'inline-block', 'border':'2px solid #2196F3', 'border-radius':'8px', 'margin':'5px', 'padding':'10px'},
            inputStyle = {"margin-left":"5px", "margin-right":"5px", 'background_color':'lightblue'},  # Padding for the options.
            style={'display':'flex','flexDirection':'row','justifyContent':'space-between'},
            className='radio-buttons'
        )),
    html.Hr(),
    dash_table.DataTable(id='datatable-id',
                         columns=[
                            #{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
                            {"name": "First Name", "id":"first_name", "deletable": False, "selectable": True},
                            {"name": "Last Name", "id":"last_name", "deletable": False, "selectable": True},
                            {"name": "Account Nickname", "id":"account_nickname", "deletable": False, "selectable": True},
                            {"name": "Account Class", "id":"account_class", "deletable": False, "selectable": True},
                            {"name": "Account Value", "id":"account_value", "deletable": False, "selectable": True},
                            {"name": "Cash Available", "id":"cash_available", "deletable": False, "selectable": True},
                            {"name": "YTD Distributions", "id":"ytd_distributions", "deletable": False, "selectable": True},
                            {"name": "RMD Amount", "id":"rmd_amount", "deletable": False, "selectable": True},
                            {"name": "Days since Last Review", "id":"days_since_last_review", "deletable": False, "selectable": True}
                        ],
                         data=df.to_dict('records') if df is not None else {},
                         editable=False,
                         filter_action="native",
                         sort_action="native",
                         sort_mode="multi",
                         column_selectable=False,
                         row_selectable="single",
                         selected_rows=[0],
                         row_deletable=False,
                         selected_columns=[],
                         page_action="native",
                         page_current=0,
                         page_size=50
                        ),
    html.Br(),
    html.Hr(),
# #This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    # html.Div(className='row',
         # style={'display' : 'flex'},
             # children=[
        # html.Div(
            # id='graph-id',
            # className='col s12 m6',
            # ),
        # # We won't be using a geolocation chart anymore.
        # #html.Div(
        # #    id='map-id',
        # #    className='col s12 m6',
        # #    )
            # ])
])

app.layout = html.Div([
    dcc.Store(id='login-state', data='login'),
    dcc.Location(id='url'),
    
    html.Div(id='login-layout', style={'display':'block'}, children=[
        loginLayout
    ]),
    html.Div(id='dashboard-layout', style={'display':'none'}, children=[
        dashboardLayout
    ])
])

#######################################################################################################################################

######################################################
# Function, Callback, Layout Definitions
######################################################

#######################################################################################################################################

#############################################
# Login Callbacks
#############################################

# Pass the login credentials that were input into the SecurityLayer for verification.
@app.callback(
    Output('login-state', 'data'),              # Updates the dcc.Store login-state on success.
    [Input('login-button', 'n_clicks')],     # Activates upon the login-button's 'n_clicks' value changing
    # Pulls the value of these inputs as arguments for the function.
    [State('login-state', 'data'), State('username-input', 'value'), State('password-input', 'value')],
    prevent_initial_call=True
)
def AuthenticateUser(n_clicks, loginState, username, password):
    print(f"Login button click detected. Authenticating {username} input credentials.")
    # Only authenticate once the login button has been clicked
    if n_clicks > 0:
        # Request the security layer authenticate the provided credentials.
        # Returns True on valid credentials, False otherwise.
        if sl.AuthenticateUser(username, password):
            # Login successful
            print(f"Login validation successful for user {username}.")
            # Store the security token from the security layer.
            session = sl.LoginSuccess(username)
            # Initialize the CRUD layer using the verified credentials
            InitializeCRUDLayer(username, password, session)
            # Return the string that requests the dashboard layout.
            return "dashboard"
        else:
            # Login failed
            print(f"Login validation failed for user {username}.")
            # Report the login failure.
            sl.LoginFailure(username)
            return "failedLogin"
    # If somehow we get here and don't have the credentials to login, return to the login layout.
    else:
        return "login"
        
# Update a div indicating a failed login.
@app.callback(
    Output('loginResult', 'children'),              # Updates the loginResult div with the return result
    Input('login-state', 'data')     # Triggers when the login-state is updated after a failed login
)
def UpdateLoginResults(loginState):
    print("Updating login results.")
    if (loginState == "failedLogin"):
        return html.Div("Login failed. Incorrect username or password.")

# Function to initialize CRUD layer. Called only after login verification of the credentials is successful.
def InitializeCRUDLayer(username, password, token):
    
    # Pull references to these from the overall program to prevent them from being locked in this scope.
    global db
    global df
    
    try:
        print(f"Initializing CRUD layer.")
        db = ClientDataCRUD(sl, token, username, password)
        print(f"Initializing mergeRead.")
        df = mergeRead()
        return html.Div("CRUD layer initialized.")
    
    except errors.OperationFailure as operationFailure:
        print(f"Operation failure: {operationFailure}")
    except Exception as exception:
        print(f"An unexpected exception occurred: {exception}") 
        
    return html.Div()

# Finally, After login verification, return the correct layout based on the login result.
@app.callback(
    Output('login-layout', 'style'),
    Output('dashboard-layout', 'style'),
    Input('login-state', 'data')
)
def SwitchLayout(loginState):
    # The login function should return either "/login" or "/dashboard" for a failed or successful login respectively.
    print(f"Login state is {loginState}")
    if loginState == "login" or loginState == "failedLogin":    
        print(f"Displaying login layout.")
        # We return both of the layouts simultaneously through the callback.
        # Doing it this way allows us to establish callbacks with references in both layouts
        # while only displaying one to avoid errors.
        # Returning these dictionaries changes which one is displayed based on the order.
        return {'display': 'block'}, {'display': 'none'}
    elif loginState == "dashboard":
        print(f"Displaying base dashboard layout.")
        return {'display': 'none'}, {'display': 'block'}
    # Good practice to have a default else case, though. Just in case.
    else:
        return {'display': 'block'}, {'display': 'none'}

#######################################################################################################################################



###########################
# Data Manipulation / Model
###########################

# The mergeRead function reduces redundancy, since we'll need to pull data like this quite often for most dashboard purposes.
# It will let us request data and strip it of ObjectIds before it goes to the dashboard.
def mergeRead(filter_data=None):

    if db is None:
        print("MergeRead called before database connection. Returning.")
        return
        
    if filter_data is None:
        print("Filter data is empty. Returning all results.")
        filter_data = {}
        
    print(f"MergeRead called. filter_data: {filter_data}")
    # Since the dashboard will be using data from both collections, we'll get data frames from both collections according to the requisite data.
    accounts_df = pd.DataFrame(db.read("accounts",filter_data))
    clients_df = pd.DataFrame(db.read("clients",{}))
    
    # We'll merge the two into a single data frame based on the shared client_id fields.
    merged_df = pd.merge(accounts_df, clients_df, left_on="client_id", right_on="_id", how="left")
        
    # Finally, we'll double-check and make sure to strip the ObjectId fields before returning it. inplace allows us to do so with the existing data object.
    merged_df.drop(columns=['_id_x', '_id_y', 'client_id'],inplace=True)
    
    # But wait, there's more! This is a good place to insert derived values that depend on both the client and account data.
    # We're just going to add days_since_last_review here but this would be a good place for other elements too.
    
    # First we have to convert the last_review_date to a proper datetime
    merged_df['last_review_date'] = pd.to_datetime(merged_df['last_review_date'])
    
    # Now we get the difference between the last_review_date and today. We'll make a new, temporary column to store the days_since_last_review field.
    today = datetime.now()
    merged_df['days_since_last_review'] = (today - merged_df['last_review_date']).dt.days
    
    # With the derived data added, we're now safe to return the data for any use.
    
    return merged_df

###########################
# Dashboard Callbacks
###########################
   
# Update Dashboard on filter application
@app.callback(
    Output('datatable-id','data'),
    [Input('filter-type', 'value')]
)
def update_dashboard(filter_type):
    print(f"Attempting to update_dashboard. Filter type: {filter_type}")
    
    # We prepared various filter options for accounts and clients, as well as a reset option. We will need to implement filters for each of these options using the 'value' we designated for each button.
    
    # Retirement Accounts
    if filter_type == 'retirement':
        # Using the same setup that called the records before, we can apply the specific filter details.
        df = pd.DataFrame(mergeRead({
            "account_class": "retirement"
        }))    
        #df.drop(columns=['_id', 'client_id'],inplace=True)

    # Non-Retirement Accounts
    elif filter_type == 'nonRetirement':
        # Each filter functions the same as the first but with different filter details.
        df = pd.DataFrame(mergeRead({
            "account_class": "non-retirement"
        }))
        
        # Using a similar action as the RMDs editing columns, we can drop irrelevant details.
        # df.drop(columns=['rmd_amount'], inplace=True)
    
    # Required Minimum Distributions
    elif filter_type == "RMDs":
        df = pd.DataFrame(mergeRead({
            "account_class": "retirement",
            "rmd_amount":{"$gt":0}        # An RMD amount should only be calculated for eligible accounts, so we can just look for a positive value.
        }))
        
        # This would be enough if we just wanted to display the matching accounts, but I want to do more.
        # To add an "RMD Met?" column, we can just add one.
        # df["RMD Met?"] = np.where(df['rmd_amount'] <= df['ytd_distributions'],"TRUE","NOT MET")
        # We can also drop the irrelevant column(s).
        # df.drop(columns=['days_since_last_review'], inplace=True)
        
    # Overdue Reviews - accounts with days_since_last_review over 365.
    # However, days_since_last_review is best as a derived value, so it isn't stored.
    # This makes the request a little more complicated, but not by much.
    elif filter_type == "reviews":
        # MergeRead derives the information for us, but since it's derived, we can't submit it as a filter, so we have to get the whole group and then do our own filtering.
        df = pd.DataFrame(mergeRead())
        df = df[df["days_since_last_review"] >= 365]
        
        #df.drop(columns=['_id', 'client_id'],inplace=True)

#   Keeping one of the original filters commented out for reference.
        
#    elif filter_type == "indivRescue":
#        df = pd.DataFrame.from_records(db.read("accounts",{
#            "animal_type": "Dog",
#            "breed":{"$in":["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
#            "sex_upon_outcome":"Intact Male",
#            "age_upon_outcome_in_weeks":{"$gte":20,"$lte":300},
#            "outcome_type":{"$ne":"Euthanasia"}
#        }))
#        df.drop(columns=['_id', 'client_id'],inplace=True)
       
    # Reset
    else:
        # For reset, it doesn't really matter whether it matches the 'reset' value or not.
        # Since the result of a reset shows everything, it works just fine to only check for the specific filters
        # and treat all other results as a reset command.
        # To reset we just need to remove the filters, so we just need to get the 'all records' read again.
        df = pd.DataFrame(mergeRead())
        #df.drop(columns=['_id', 'client_id'],inplace=True)

    # Now we just need to return the data to be displayed per the provided specifications
    #columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    data=df.to_dict('records')
    
    #return (data,columns)
    # print(f"Data returning from update_dashboard callback: {data}")
    return data
    
#############################################
# Interaction Between Components / Controller
# Style Callbacks
#############################################

# Update Label Styles on Click
@app.callback(
    Output('filter-type', 'inputStyle'),
    [Input('filter-type', 'value')]
)
def update_label_style(selected_value):
    print(f"Attempting to update_label_style.")
    default_style = {'background-color': 'lightblue', 'margin-left': '5px', 'margin-right': '5px'}
    selected_style = {'background-color': 'darkblue', 'margin-left': '5px', 'margin-right': '5px'}
 
    return selected_style if selected_value != 'reset' else default_style

# Highlight a cell on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    print(f"Attempting to update_styles.")
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]
    
# Display the breeds of animal based on quantity represented in
# the data table
# @app.callback(
    # Output('graph-id', "children"),
    # [Input('datatable-id', "derived_virtual_data")])
# def update_graphs(viewData):
    # print(f"Attempting to update_graphs.")
    # ###FIX ME ####
    # # add code for chart of your choice (e.g. pie chart) #

    # # Good practice to ensure the data is present before operating on it.
    # if viewData is None:
        # return []
    
    # # We'll show the distribution of breeds among the filtered selection.
    # # However, when unfiltered this will be a mess because there are a ton of dog and cat breeds in the data.
    # # So we'll just show the top 10 most common results and bundle the rest into an 'Others' category.
    
    # # First, we need to get a DataFrame from the viewData
    # dfData = pd.DataFrame.from_dict(viewData)
    
    # # The full data includes an animal_type for Other, which we don't need to worry about.
    # dfData = dfData[dfData["animal_type"].isin(["Dog","Cat"])]
    
    # # Count the breeds in the filtered data so that we can calculate their frequency
    # breedPercent = dfData["breed"].value_counts(normalize=True) * 100
    
    # # Bundle the top 10 breeds into a data frame.
    # topResults = breedPercent.head(10)
    # topResultsDF = pd.DataFrame({"breed":topResults.index, "percentage":topResults.values})
    
    # # Each filter uses less than 10 breeds, so let's check to make sure there are more than 10.
    # if len(breedPercent) > 10:
        # # If so, we bundle anything outside of the top 10 into the 'Others' category.
        # othersPercent = breedPercent[10:].sum()
        # othersDF = pd.DataFrame({"breed":["Others"],"percentage":[othersPercent]})
        # topResultsDF = pd.concat([topResultsDF, othersDF], ignore_index=True)
    
    # # And then we just return those results.
    # return [
        # dcc.Graph(            
            # figure = px.pie(topResultsDF, names='breed', values="percentage", title='Top Breeds by Percentage')
        # )    
    # ]
    
# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of 
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
# @app.callback(
    # Output('map-id', "children"),
    # [Input('datatable-id', "derived_virtual_data"),
     # Input('datatable-id', "derived_virtual_selected_rows")])
# def update_map(viewData, index):  
    # print(f"Attempting to update_map.")
    # if viewData is None:
        # return
    # elif index is None:
        # return
    
    # dff = pd.DataFrame.from_dict(viewData)
    # # Because we only allow single row selection, the list can be converted to a row index here
    # if index is None:
        # row = 0
    # else: 
        # row = index[0]
        
    # # Austin TX is at [30.75,-97.48]
    # return [
        # dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            # dl.TileLayer(id="base-layer-id"),
            # # Marker with tool tip and popup
            # # Column 13 and 14 define the grid-coordinates for the map
            # # Column 4 defines the breed for the animal
            # # Column 9 defines the name of the animal
            # dl.Marker(position=[dff.iloc[row,13],dff.iloc[row,14]], children=[
                # dl.Tooltip(dff.iloc[row,4]),
                # dl.Popup([
                    # html.H1("Animal Name"),
                    # html.P(dff.iloc[row,9])
                # ])
            # ])
        # ])
    # ]

#######################################################################################################################################
#######################################################################################################################################

#########################
# Runtime Completion
# app.run_server must be called last.
#########################

app.run_server(debug=False)