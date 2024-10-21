# Project: **Remote Work and Mental Health Dashboard**

## Overview
This project analyzes the impact of remote work on mental health using a dataset housed in MongoDB. The focus is on understanding how various factors, such as **job role**, **work location**, and **stress levels**, influence employees' mental well-being. Through data cleaning, interactive analysis, and visualizations, we derive insights that can help organizations better support their remote workforce.

This project is built using **Flask** for the backend, **Plotly** for interactive visualizations, and **MongoDB** as the database to store and retrieve the dataset.

## Objectives
1. **Identify trends in mental health conditions across different job roles.**
2. **Analyze the relationship between work-life balance and hours worked per week.**
3. **Examine how mental health conditions influence productivity changes.**
4. **Provide users with interactive, filterable dashboards to explore data based on job role, region, and work location.**

## Features

The project includes an interactive web application where users can explore insights related to mental health, work-life balance, and productivity. Users can apply filters to focus on specific **job roles**, **regions**, and **work locations** (remote, hybrid, onsite).

## Data Source
The dataset is stored in **MongoDB** and is sourced from the following Kaggle dataset: [Remote Work and Mental Health](https://www.kaggle.com/datasets/waqi786/remote-work-and-mental-health).

## Visualizations

### 1. **Mental Health Conditions by Job Role**
- **Type**: Bar chart
- **Library**: Plotly
- **Interaction**: Dropdown to filter by job role, region, and work location.
- **Description**: This visualization displays the number of employees experiencing various mental health conditions (e.g., anxiety, depression) across different job roles. Users can filter by job role, region, or work location to understand how these factors influence mental health.

### 2. **Work-Life Balance vs. Hours Worked**
- **Type**: Scatter plot
- **Library**: Plotly
- **Interaction**: Dropdown to filter by job role, region, and work location.
- **Description**: This scatter plot illustrates the relationship between hours worked per week and work-life balance ratings. The data is color-coded by stress levels, helping users visualize how working hours impact employees' perception of work-life balance. Filters for job role, region, and work location allow users to focus on specific groups of employees.

### 3. **Productivity Change by Mental Health Condition**
- **Type**: Stacked bar chart
- **Library**: Plotly
- **Interaction**: Dropdown to filter by job role, region, and work location.
- **Description**: This stacked bar chart shows how productivity changes (increase, decrease, or no change) are distributed across different mental health conditions. Users can apply filters to explore how job role, region, or work location influences the relationship between mental health and productivity.

## Methodology
1. **Data Storage**: The dataset is stored in MongoDB for efficient retrieval and filtering based on user input.
2. **Data Cleaning**: Missing values are handled, outliers are managed, and categorical data (e.g., job roles, work locations) are standardized for consistency.
3. **Data Filtering**: The app allows users to filter data by **Job Role**, **Region**, and **Work Location**. Selecting "All" in any filter will consider all records for that filter.
4. **Visualization**: Plotly is used to generate interactive, dynamic visualizations that adjust based on user input. The dashboard allows users to explore multiple aspects of the data seamlessly.

## Technology Stack
- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Visualizations**: Plotly (for interactive charts)
- **Frontend**: HTML, Bootstrap, JavaScript, jQuery (for AJAX requests)

## Ethical Considerations
We are committed to ensuring that all data handling and analysis adhere to ethical standards. This includes:
- **Data Privacy**: We ensure that personal information in the dataset is anonymized, protecting the privacy of individuals.
- **Mindful Reporting**: We recognize that mental health is a sensitive topic and are careful to avoid stigmatizing language when interpreting results.

## References
- Kaggle Dataset: [Remote Work and Mental Health](https://www.kaggle.com/datasets/waqi786/remote-work-and-mental-health)
- Flask Documentation: [Flask](https://flask.palletsprojects.com/)
- Plotly Documentation: [Plotly](https://plotly.com/python/)
- MongoDB Documentation: [MongoDB](https://www.mongodb.com/)
- Bootstrap Documentation: [Bootstrap](https://getbootstrap.com/)



 
