# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports for dashboard components
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from AnimalShelter import AnimalShelter

###########################
# Data Manipulation / Model
###########################
# FIX ME update with your username and password and CRUD Python module name

username = "aacuser"
password = "SNHU1234"

# Connect to database via CRUD Module
db = AnimalShelter(username, password)

# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(db.read({}))

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)

df.drop(columns=['_id'],inplace=True)
# The AnimalShelter's read function was updated to drop the _id column before returning.

## Debug
# print(len(df.to_dict(orient='records')))
# print(df.columns)


#########################
# Dashboard Layout / View
#########################
app = JupyterDash(__name__)

#FIX ME Add in Grazioso Salvare’s logo
image_filename = '6 - Grazioso Salvare Logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
#    html.Div(id='hidden-div', style={'display':'none'}),
    #FIX ME Place the HTML image tag in the line below into the app.layout code according to your design
    #FIX ME Also remember to include a unique identifier such as your name or date
    html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                         style={'max-width':'200px', 'max-height':'200px'})),
    html.Center(html.B(html.H1('CS-340 Dashboard'))),
    html.Center(html.H3('Written by Jason Holmes')),
    html.Hr(),
    html.Div(
        #FIXME Add in code for the interactive filtering options. For example, Radio buttons, drop down, checkboxes, etc.
        dcc.RadioItems(
            id='filter-type',
            options=[
                {'label': 'Water Rescue', 'value':'waterRescue'},
                {'label': 'Mountain & Wilderness Rescue', 'value':'wildRescue'},
                {'label': 'Disaster & Individual Rescue', 'value':'indivRescue'},
                {'label': 'Reset Filters', 'value':'reset'}
            ],
            value='reset', # Default input
            inputStyle = {"margin-left":"20px", "margin-right":"20px"}  # Padding for the options.
        )),
    html.Hr(),
    dash_table.DataTable(id='datatable-id',
                         columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
                         data=df.to_dict('records'),
#FIXME: Set up the features for your interactive data table to make it user-friendly for your client
#If you completed the Module Six Assignment, you can copy in the code you created here 
                         selected_rows=[0],
                         editable=False,
                         filter_action="native",
                         sort_action="native",
                         sort_mode="multi",
                         column_selectable=False,
                         row_selectable="single",
                         row_deletable=False,
                         selected_columns=[],
                         page_action="native",
                         page_current=0,
                         page_size=15
                        ),
    html.Br(),
    html.Hr(),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',
            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################

@app.callback(Output('datatable-id','data'),
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
    # FIX ME Add code to filter interactive data table with MongoDB queries
    #
    #        
    #        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    #        data=df.to_dict('records')
    #       
    #       
    #        return (data,columns)
    # We prepared filter options for water rescue, mountain/wilderness rescue, disaster rescue & individual tracking, and a reset option.
    # We will need to implement filters for each of these buttons using the 'value' we designated for each button.
    # Water Rescue
    if filter_type == 'waterRescue':
        # Using the same setup that called the records before, we can apply the specific filter details.
        df = pd.DataFrame.from_records(db.read({
            "animal_type": "Dog",
            "breed":{"$in":["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
            "sex_upon_outcome":"Intact Female",
            "age_upon_outcome_in_weeks":{"$gte":26,"$lte":156},
            # We also don't want to include any entries where the patient was euthanised.
            "outcome_type":{"$ne":"Euthanasia"}
        }))
        
        df.drop(columns=['_id'],inplace=True)

    # Mountain/Wilderness Rescue
    elif filter_type == 'wildRescue':
        # Each filter functions the same as the first but with different filter details.
        df = pd.DataFrame.from_records(db.read({
            "animal_type": "Dog",
            "breed":{"$in":["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
            "sex_upon_outcome":"Intact Male",
            "age_upon_outcome_in_weeks":{"$gte":26,"$lte":156},
            "outcome_type":{"$ne":"Euthanasia"}
        }))
        df.drop(columns=['_id'],inplace=True)
    
    # Disaster Rescue & Individual Tracking
    elif filter_type == "indivRescue":
        df = pd.DataFrame.from_records(db.read({
            "animal_type": "Dog",
            "breed":{"$in":["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
            "sex_upon_outcome":"Intact Male",
            "age_upon_outcome_in_weeks":{"$gte":20,"$lte":300},
            "outcome_type":{"$ne":"Euthanasia"}
        }))
        df.drop(columns=['_id'],inplace=True)
    
    # Reset
    else:
        # For reset, it doesn't really matter whether it matches the 'reset' value or not.
        # Since the result of a reset shows everything, it works just fine to only check for the specific filters
        # and treat all other results as a reset command.
        # To reset we just need to remove the filters, so we just need to get the 'all records' read again.
        df = pd.DataFrame.from_records(db.read({}))
        df.drop(columns=['_id'],inplace=True)

    # Now we just need to return the data to be displayed per the provided specifications
    #columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    data=df.to_dict('records')
    
    #return (data,columns)
    return data
    
    
# Display the breeds of animal based on quantity represented in
# the data table
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")])
def update_graphs(viewData):
    ###FIX ME ####
    # add code for chart of your choice (e.g. pie chart) #

    # Good practice to ensure the data is present before operating on it.
    if viewData is None:
        return []
    
    # We'll show the distribution of breeds among the filtered selection.
    # However, when unfiltered this will be a mess because there are a ton of dog and cat breeds in the data.
    # So we'll just show the top 10 most common results and bundle the rest into an 'Others' category.
    
    # First, we need to get a DataFrame from the viewData
    dfData = pd.DataFrame.from_dict(viewData)
    
    # The full data includes an animal_type for Other, which we don't need to worry about.
    dfData = dfData[dfData["animal_type"].isin(["Dog","Cat"])]
    
    # Count the breeds in the filtered data so that we can calculate their frequency
    breedPercent = dfData["breed"].value_counts(normalize=True) * 100
    
    # Bundle the top 10 breeds into a data frame.
    topResults = breedPercent.head(10)
    topResultsDF = pd.DataFrame({"breed":topResults.index, "percentage":topResults.values})
    
    # Each filter uses less than 10 breeds, so let's check to make sure there are more than 10.
    if len(breedPercent) > 10:
        # If so, we bundle anything outside of the top 10 into the 'Others' category.
        othersPercent = breedPercent[10:].sum()
        othersDF = pd.DataFrame({"breed":["Others"],"percentage":[othersPercent]})
        topResultsDF = pd.concat([topResultsDF, othersDF], ignore_index=True)
    
    # And then we just return those results.
    return [
        dcc.Graph(            
            figure = px.pie(topResultsDF, names='breed', values="percentage", title='Top Breeds by Percentage')
        )    
    ]
    
#This callback will highlight a cell on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
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
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(viewData, index):  
    if viewData is None:
        return
    elif index is None:
        return
    
    dff = pd.DataFrame.from_dict(viewData)
    # Because we only allow single row selection, the list can be converted to a row index here
    if index is None:
        row = 0
    else: 
        row = index[0]
        
    # Austin TX is at [30.75,-97.48]
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            # Column 13 and 14 define the grid-coordinates for the map
            # Column 4 defines the breed for the animal
            # Column 9 defines the name of the animal
            dl.Marker(position=[dff.iloc[row,13],dff.iloc[row,14]], children=[
                dl.Tooltip(dff.iloc[row,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[row,9])
                ])
            ])
        ])
    ]
app.run_server(debug=True)
