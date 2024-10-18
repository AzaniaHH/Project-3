from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from pymongo import MongoClient
import io
import base64

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['remote_work_db']
collection = db['mental_health']

# Retrieve and clean data
data = pd.DataFrame(list(collection.find()))
data['Job_Role'] = data['Job_Role'].str.title()
data['Region'] = data['Region'].str.title()
data['Work_Location'] = data['Work_Location'].str.capitalize()
data['Stress_Level'] = data['Stress_Level'].str.capitalize()

# Home route
@app.route('/')
def index():
    # Get unique values for dropdown menus
    job_roles = sorted(data['Job_Role'].unique())
    stress_levels = sorted(data['Stress_Level'].unique())
    work_locations = sorted(data['Work_Location'].unique())

    return render_template('index.html', job_roles=job_roles, stress_levels=stress_levels, work_locations=work_locations)

# Route to generate the heatmap based on Stress Level and Work Location
@app.route('/heatmap', methods=['POST'])
def heatmap():
    stress_level = request.form.get('stress_level')
    work_location = request.form.get('work_location')

    # Filter data based on stress level and work location
    filtered_data = data[(data['Stress_Level'] == stress_level) & (data['Work_Location'] == work_location)]

    # Pivot the data to create a heatmap (Job_Role vs Hours_Worked_Per_Week)
    pivot_table = filtered_data.pivot_table(index='Job_Role', values='Hours_Worked_Per_Week', aggfunc='mean')

    # Create heatmap with Seaborn
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, cmap='RdYlGn', annot=True, linewidths=.5)
    plt.title(f'Heatmap of Hours Worked for {stress_level} and {work_location}')

    # Convert the heatmap to PNG for display
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return jsonify({'plot': plot_url})

# Route to generate correlation graph between Job Role, Stress Level, and Mental Health
@app.route('/correlation', methods=['POST'])
def correlation():
    job_role = request.form.get('job_role')

    # Filter data by job role
    filtered_data = data[data['Job_Role'] == job_role]

    # Create a scatter plot of Stress Level vs Mental Health Condition
    fig = px.scatter(filtered_data, x='Stress_Level', y='Mental_Health_Condition',
                     color='Mental_Health_Condition', hover_data=['Hours_Worked_Per_Week'],
                     title=f'Stress Level vs Mental Health for {job_role}')

    plot_html = fig.to_html(full_html=False)
    return jsonify({'plot_html': plot_html})

# Route for Hours Worked vs. Stress Level scatter plot
@app.route('/hours_vs_stress', methods=['POST'])
def hours_vs_stress():
    job_role = request.form.get('job_role')

    # Filter data by job role
    filtered_data = data[data['Job_Role'] == job_role]

    # Create a scatter plot
    fig = px.scatter(filtered_data, x='Hours_Worked_Per_Week', y='Stress_Level',
                     color='Stress_Level', title=f'Hours Worked vs Stress Level for {job_role}')

    plot_html = fig.to_html(full_html=False)
    return jsonify({'plot_html': plot_html})

# Route for Job Role vs. Stress Level bar chart
@app.route('/jobrole_vs_stress', methods=['POST'])
def jobrole_vs_stress():
    # Filter data by stress level
    filtered_data = data.groupby('Job_Role')['Stress_Level'].value_counts().unstack().fillna(0)

    # Create a bar chart using Plotly
    fig = px.bar(filtered_data, barmode='group', title='Job Role vs Stress Level')

    plot_html = fig.to_html(full_html=False)
    return jsonify({'plot_html': plot_html})

if __name__ == '__main__':
    app.run(debug=True)























