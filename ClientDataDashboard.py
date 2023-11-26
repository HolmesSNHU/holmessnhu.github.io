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

# Configure the necessary Python module imports for dashboard components
from dash import Dash
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64
from datetime import datetime

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt

# Import CRUD interface layer
from ClientDataCRUD import ClientDataCRUD

# Import Security Layer
from CS499_Security import SecurityLayer

# PyMongo utilities
from pymongo import errors

###########################
# Data Manipulation / Model
###########################

# The mergeRead function reduces redundancy, since we'll need to pull data like this quite often for most dashboard purposes.
# It will let us request data and strip it of ObjectIds before it goes to the dashboard.

def mergeRead(filter_data={}):

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

# The credentials are currently hard-coded into the interface layer as well, so this is technically redundant.
# To note, however, that login details will be replaced with a login database in the future.

username = "admin"
password = "root"

# Connect to database via CRUD Module
# Whenever initiating contact with external elements, try-catch is a good idea.
try:
    db = ClientDataCRUD(username, password)

    # A problem exists wherein MongoDB will return the _id column as an ObjectId, which cannot be JSON serialized.
    # To resolve this, we need to strip any ObjectId values before they get serialized, and the simplest way to do this is to strip them as soon as they're read from the database.
    # However, we don't want to update the CRUD layer to do this because we may still want to be able to access those IDs later, so we'll define a mergeRead() function in the dashboard.
    
    df = mergeRead()    
    
except errors.OperationFailure as operationFailure:
    print(f"Operation failure: {operationFailure}")
except Exception as exception:
    print(f"An unexpected exception occurred: {exception}") 

## Debug
# print(len(df.to_dict(orient='records')))
# print(df.columns)


# Open a SecurityLayer instance. More significant adjustments will be necessary to fully implement logins.
# security = SecurityLayer()

#########################
# Dashboard Layout / View
#########################
app = Dash(__name__)

#image_filename = '6 - Grazioso Salvare Logo.png' # replace with your own image
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())

print(f"Attempting to apply base layout.")
app.layout = html.Div(style={'max-width':'80%', 'margin':'auto'}, children=[
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
                         data=df.to_dict('records'),
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

#############################################
# Interaction Between Components / Controller
#############################################

@app.callback(Output('filter-type', 'inputStyle'),
                [Input('filter-type', 'value')])
def update_label_style(selected_value):
    print(f"Attempting to update_label_style.")
    default_style = {'background-color': 'lightblue', 'margin-left': '5px', 'margin-right': '5px'}
    selected_style = {'background-color': 'darkblue', 'margin-left': '5px', 'margin-right': '5px'}
 
    return selected_style if selected_value != 'reset' else default_style

@app.callback(Output('datatable-id','data'),
              [Input('filter-type', 'value')])
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
    
#This callback will highlight a cell on the data table when the user selects it
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
app.run_server(debug=False)