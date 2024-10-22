from flask import Flask
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

# Initialize Flask app
server = Flask(__name__)

# Initialize Dash app
app = Dash(__name__, server=server, url_base_pathname='/')

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['remote_work_db']  # Database
collection = db['mental_health']  # Collection

# Retrieve data from MongoDB
data = pd.DataFrame(list(collection.find()))

# Clean the data (replace NaNs)
data['Mental_Health_Condition'] = data['Mental_Health_Condition'].fillna('None')
data['Physical_Activity'] = data['Physical_Activity'].fillna('None')

# Dash layout
app.layout = html.Div([
    html.H1(
        "Remote vs Onsite Work Analysis",
        style={'textAlign': 'center', 'fontSize': '60px', 'padding': '40px'}  # Title size
    ),

    # Move the label above the dropdown menu
    html.Div([
        html.Div([
            html.Label(
                "Select Work Location:",
                style={'fontSize': '22px', 'paddingBottom': '10px', 'display': 'block'}  # Block to put label above dropdown
            ),
            dcc.Dropdown(
                id='work-location-dropdown',
                options=[
                    {'label': 'Remote', 'value': 'Remote'},
                    {'label': 'Onsite', 'value': 'Onsite'},
                    {'label': 'Hybrid', 'value': 'Hybrid'}
                ],
                value='Remote',
                style={'width': '50%', 'fontSize': '24px', 'marginBottom': '20px'}
            )
        ], style={'textAlign': 'center', 'paddingBottom': '30px'}) 
    ]),

    # Graphs layout
    html.Div([
        dcc.Graph(id='stress-level-chart', style={'width': '70%', 'margin': 'auto', 'padding': '20px'}),
        dcc.Graph(id='work-life-balance-chart', style={'width': '70%', 'margin': 'auto', 'padding': '20px'}),
        dcc.Graph(id='mental-health-chart', style={'width': '70%', 'margin': 'auto', 'padding': '20px'})
    ], style={'textAlign': 'center', 'paddingBottom': '50px'}) 
])


# Callback for updating all three charts
@app.callback(
    [Output('stress-level-chart', 'figure'),
     Output('work-life-balance-chart', 'figure'),
     Output('mental-health-chart', 'figure')],
    [Input('work-location-dropdown', 'value')]
)
def update_charts(work_location):
    # Filter data based on selected work location
    filtered_data = data[data['Work_Location'] == work_location]

    # Visualization 1: Stress Levels by Work Location
    stress_fig = px.histogram(
        filtered_data,
        x='Stress_Level',
        title=f'Stress Levels for {work_location} Workers',
        labels={'Stress_Level': 'Stress Level', 'Count': 'Number of Employees'},
        color_discrete_sequence=['#3b5998']  
    )
    stress_fig.update_layout(
        title_font_size=26,  
        xaxis_title_font_size=22,
        yaxis_title_font_size=22,
        font=dict(size=18),  # General font size 
        margin=dict(l=40, r=40, t=60, b=40),  # Margins
        height=350,  # Height
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Background Color
        paper_bgcolor='rgba(255, 255, 255, 1)',  # Background Color
        hoverlabel=dict(  # Customize hover label
            font_size=20,  # Hover text font size
            bgcolor="white",  # Set background color of hover text
            font_color="black"  # Set hover text color
        )
    )

    # Visualization 2: Work-Life Balance Ratings by Work Location
    balance_fig = px.box(
        filtered_data,
        x='Work_Location',
        y='Work_Life_Balance_Rating',
        title=f'Work-Life Balance for {work_location} Workers',
        labels={'Work_Location': 'Work Location', 'Work_Life_Balance_Rating': 'Rating'},
        color_discrete_sequence=['#ff7f0e']  
    )
    balance_fig.update_layout(
        title_font_size=26,
        xaxis_title_font_size=20,
        yaxis_title_font_size=20,
        font=dict(size=18),
        margin=dict(l=40, r=40, t=60, b=40),
        height=350,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(255, 255, 255, 1)',
        hoverlabel=dict(
            font_size=20,  # Hover Text Font Size
            bgcolor="white",  # Hover Background
            font_color="black"  # Hover Text Color
        )
    )

    # Visualization 3: Mental Health Condition Distribution
    mental_health_fig = px.pie(
        filtered_data,
        names='Mental_Health_Condition',
        title=f'Mental Health Conditions for {work_location} Workers',
        color_discrete_sequence=px.colors.qualitative.Pastel  
    )
    mental_health_fig.update_layout(
        title_font_size=26,
        font=dict(size=18),
        margin=dict(l=40, r=40, t=60, b=40),
        height=350,
        legend=dict(font=dict(size=20)),  #Legend Font Size
        hoverlabel=dict(
            font_size=20,  # Hover Text Font Size
            bgcolor="white",  # Hover Background Color
            font_color="black"  # Gover Text Color
        )
    )

    return stress_fig, balance_fig, mental_health_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)












