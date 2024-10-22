from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
app = Flask(__name__)
# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['remote_work_db']
collection = db['mental_health']
data = pd.DataFrame(list(collection.find()))
# Clean the data (ensure Job_Role and Region are properly formatted)
data['Job_Role'] = data['Job_Role'].str.title()
data['Region'] = data['Region'].str.title()
@app.route('/')
def index():
    # Get unique values for dropdowns from the data
    job_roles = sorted(data['Job_Role'].unique())
    regions = sorted(data['Region'].unique())
    # Add "All" option for Job Role and Region
    job_roles.insert(0, "All")
    regions.insert(0, "All")
    return render_template('index.html', job_roles=job_roles, regions=regions)
@app.route('/plot', methods=['POST'])
def plot():
    job_role = request.form.get('job_role')
    region = request.form.get('region')
    gender = request.form.get('gender')
    # Debugging: Print the received values
    print(f"Job Role: {job_role}, Region: {region}, Gender: {gender}")
    # Check if any field is missing
    if not job_role or not region or not gender:
        return jsonify({'error': 'Please select valid filters for Job Role, Region, and Gender.'}), 400
    # Filter data based on the inputs
    filtered_data = data[
        ((data['Job_Role'] == job_role) if job_role != 'All' else True) &
        ((data['Region'] == region) if region != 'All' else True) &
        ((data['Gender'] == gender) if gender != 'All' else True)
    ]
    if filtered_data.empty:
        return jsonify({'error': 'No data found for the selected filters.'}), 400
    # Generate scatter plot: Work-Life Balance vs Hours Worked
    scatter_fig = px.scatter(filtered_data, x='Hours_Worked_Per_Week', y='Work_Life_Balance_Rating',
                             color='Stress_Level', hover_data=['Mental_Health_Condition'],
                             title=f'Work-Life Balance vs Hours Worked for {job_role} in {region}')
    scatter_plot_html = scatter_fig.to_html(full_html=False)
    # Generate bar chart: Stress Levels Distribution by Job Role
    bar_fig = px.bar(filtered_data, x='Stress_Level', color='Stress_Level',
                     title=f'Stress Level Distribution for {job_role} in {region}',
                     labels={'count': 'Number of Employees'})
    bar_chart_html = bar_fig.to_html(full_html=False)
    # Generate pie chart: Mental Health Condition Distribution
    pie_fig = px.pie(filtered_data, names='Mental_Health_Condition',
                     title=f'Mental Health Condition Distribution for {job_role} in {region}')
    pie_chart_html = pie_fig.to_html(full_html=False)
    # Return all three plots as a JSON response
    return jsonify({
        'scatter_plot_html': scatter_plot_html,
        'bar_chart_html': bar_chart_html,
        'pie_chart_html': pie_chart_html
    })
if __name__ == '__main__':
    app.run(debug=True)







