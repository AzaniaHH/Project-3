from flask import Flask, render_template, request, jsonify
import pandas as pd
from pymongo import MongoClient
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['remote_work_db']
collection = db['mental_health']

# Data cleaning function
def clean_data(df):
    # Handle missing values and standardize categories
    df['Mental_Health_Condition'] = df['Mental_Health_Condition'].fillna('None')
    df['Physical_Activity'] = df['Physical_Activity'].fillna('None')
    df['Gender'] = df['Gender'].str.capitalize()
    df['Job_Role'] = df['Job_Role'].str.title().replace({'Hr': 'HR'})
    df['Industry'] = df['Industry'].str.title().replace({'It': 'IT'})
    df['Work_Location'] = df['Work_Location'].str.capitalize()
    df['Stress_Level'] = df['Stress_Level'].str.capitalize().replace({'Low ': 'Low'})
    df['Productivity_Change'] = df['Productivity_Change'].str.title()
    df['Satisfaction_with_Remote_Work'] = df['Satisfaction_with_Remote_Work'].str.title()
    df['Access_to_Mental_Health_Resources'] = df['Access_to_Mental_Health_Resources'].str.capitalize()
    df['Sleep_Quality'] = df['Sleep_Quality'].str.title()
    df['Region'] = df['Region'].str.title()
    df['Hours_Worked_Per_Week'] = df['Hours_Worked_Per_Week'].clip(lower=20, upper=60)
    return df

@app.route('/')
def index():
    # Retrieve data from MongoDB to populate the dropdowns
    data = pd.DataFrame(list(collection.find()))
    data_cleaned = clean_data(data)

    # Get unique values for dropdown menus
    job_roles = sorted(data_cleaned['Job_Role'].unique())
    regions = sorted(data_cleaned['Region'].unique())
    work_locations = sorted(data_cleaned['Work_Location'].unique())
    
    return render_template('index.html', job_roles=job_roles, regions=regions, work_locations=work_locations)

@app.route('/plot', methods=['POST'])
def plot():
    # Retrieve the selected filters from the form
    job_role = request.form.get('job_role')
    region = request.form.get('region')
    work_location = request.form.get('work_location')

    # Retrieve data from MongoDB and clean it
    data = pd.DataFrame(list(collection.find()))
    data_cleaned = clean_data(data)

    # Apply filters
    if job_role != 'All':
        data_cleaned = data_cleaned[data_cleaned['Job_Role'] == job_role]
    if region != 'All':
        data_cleaned = data_cleaned[data_cleaned['Region'] == region]
    if work_location != 'All':
        data_cleaned = data_cleaned[data_cleaned['Work_Location'] == work_location]

    # If no data is found, return an error message
    if data_cleaned.empty:
        return jsonify({'error': 'No data found for the selected filters.'}), 400

    # Example: Create a Bokeh bar chart for Mental Health Conditions
    mental_health_counts = data_cleaned.groupby('Mental_Health_Condition').size().reset_index(name='count')
    source = ColumnDataSource(mental_health_counts)

    p = figure(x_range=mental_health_counts['Mental_Health_Condition'], title="Mental Health Conditions by Job Role",
               toolbar_location=None, tools="")
    p.vbar(x='Mental_Health_Condition', top='count', width=0.9, source=source)

    # Embed Bokeh plot into HTML
    script, div = components(p)

    # Return the plot as a JSON response to the frontend
    return jsonify({'plot_html': script + div})

if __name__ == '__main__':
    app.run(debug=True)



