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
db = client['remote_work_db']
collection = db['mental_health']

# Retrieve data from MongoDB
data = pd.DataFrame(list(collection.find()))

# Clean the data (replace NaNs)
data['Mental_Health_Condition'] = data['Mental_Health_Condition'].fillna('None')
data['Physical_Activity'] = data['Physical_Activity'].fillna('None')

# Dash layout
app.layout = html.Div([
    # Project Overview Section
    html.H1("Remote vs Onsite Work: Mental Health Analysis", style={'textAlign': 'center', 'fontSize': '60px', 'padding': '40px'}),
    
    html.H2("Project Overview", style={'fontSize': '40px', 'marginTop': '20px'}),
    html.P(
        """
        This dashboard explores the impact of different work environments—remote, onsite, and hybrid—on employees' mental health, stress levels, 
        and work-life balance. The analysis is based on a dataset of 5,000 employees across various industries.
        The goal is to provide insights into how different work setups affect employee well-being and help organizations make data-driven decisions 
        to improve work environments.
        """, style={'fontSize': '32px', 'marginBottom': '30px'}
    ),

    # Instructions Section
    html.H2("How to Use This Dashboard", style={'fontSize': '32px', 'marginTop': '20px'}),
    html.P(
        """
        Use the dropdown below to select the work location you would like to explore: Remote, Onsite, or Hybrid.
        The graphs will automatically update to show data on stress levels, work-life balance, and mental health conditions for the selected work location.
        """, style={'fontSize': '32px', 'marginBottom': '40px'}
    ),

    # Dropdown and Graphs Section
    html.Div([
        html.Div([
            html.Label(
                "Select Work Location:",
                style={'fontSize': '22px', 'paddingBottom': '10px', 'display': 'block'}
            ),
            dcc.Dropdown(
                id='work-location-dropdown',
                options=[
                    {'label': 'Remote', 'value': 'Remote'},
                    {'label': 'Onsite', 'value': 'Onsite'},
                    {'label': 'Hybrid', 'value': 'Hybrid'}
                ],
                value='Remote',
                style={'width': '50%', 'fontSize': '30px', 'marginBottom': '20px'}
            )
        ], style={'textAlign': 'left', 'paddingBottom': '60px'})
    ]),

    # Graphs Layout
    html.Div([
        dcc.Graph(id='stress-level-chart', style={'width': '90%', 'height': '550px', 'margin': 'auto', 'padding': '60px'}),
        dcc.Graph(id='work-life-balance-chart', style={'width': '90%', 'height': '550px', 'margin': 'auto', 'padding': '60px'}),
        dcc.Graph(id='mental-health-chart', style={'width': '90%', 'height': '550px', 'margin': 'auto', 'padding': '60px'})
    ], style={'textAlign': 'center', 'paddingBottom': '50px'}),

    # Insights Section
    html.H2("Key Insights", style={'fontSize': '34px', 'marginTop': '20px'}),
    html.Ul([
        html.Li("Remote workers generally report lower high stress levels compared to onsite workers.", style={'fontSize': '30px'}),
        html.Li("Work-life balance is significantly higher among remote workers than those working onsite.", style={'fontSize': '30px'}),
        html.Li("Hybrid workers show a balanced distribution in both stress levels and work-life balance, but variability still exists.", style={'fontSize': '30px'}),
        html.Li("Anxiety is more common among remote workers, while depression is slightly higher in onsite workers.", style={'fontSize': '30px'})
    ], style={'marginBottom': '50px'})
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
        labels={'Stress_Level': 'Stress Level', 'count': 'Number of Employees'},
        color_discrete_sequence=['#3b5998']
    )
    stress_fig.update_layout(
        title_font_size=30,
        xaxis_title_font_size=24,
        yaxis_title_font_size=24,
        font=dict(size=20),
        margin=dict(l=40, r=40, t=60, b=40),
        height=500,  # Increased height for larger graph
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(255, 255, 255, 1)',
        hoverlabel=dict(font_size=20, bgcolor="white", font_color="black")
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
        title_font_size=30,
        xaxis_title_font_size=24,
        yaxis_title_font_size=24,
        font=dict(size=20),
        margin=dict(l=40, r=40, t=60, b=40),
        height=500,  
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(255, 255, 255, 1)',
        hoverlabel=dict(font_size=20, bgcolor="white", font_color="black")
    )

    # Visualization 3: Mental Health Condition Distribution
    mental_health_fig = px.pie(
        filtered_data,
        names='Mental_Health_Condition',
        title=f'Mental Health Conditions for {work_location} Workers',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    mental_health_fig.update_layout(
        title_font_size=30,
        font=dict(size=20),
        margin=dict(l=40, r=40, t=60, b=40),
        height=700,  
        legend=dict(font=dict(size=18)),
        hoverlabel=dict(font_size=20, bgcolor="white", font_color="black")
    )

    return stress_fig, balance_fig, mental_health_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
















