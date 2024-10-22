# Remote Work vs Onsite Work: Analyzing Mental Health and Work-Life Balance

## Overview

This project explores the differences between **remote** and **onsite** work with respect to mental health, stress levels, work-life balance, and satisfaction. Using a dataset of 5,000 employees, the project visualizes key metrics that reflect the impact of work location on mental well-being and overall productivity. The analysis is presented via an interactive web dashboard built using **Flask** and **Dash**, powered by **Plotly** for interactive visualizations.

The main goal is to allow users to compare the effects of remote, onsite, and hybrid work environments on mental health, social isolation, and work-life balance. The project offers a clean and intuitive interface where users can choose the work location and explore visualized insights across multiple metrics.

## Project Features

- **Interactive Dashboard**: Users can filter visualizations based on work location (Remote, Onsite, Hybrid).
- **Three Visualizations**:
  1. **Stress Levels by Work Location**: Histogram comparing stress levels across different work setups.
  2. **Work-Life Balance by Work Location**: Box plot to assess work-life balance for different work environments.
  3. **Mental Health Conditions**: Pie chart showing the distribution of mental health conditions (e.g., depression, anxiety) among employees based on work location.

The project uses MongoDB to store and query the dataset and uses Dash for building the interactive web interface.

## Requirements

To run this project locally, you'll need the following dependencies:

- **Python 3.x**
- **Flask**: `pip install flask`
- **Dash**: `pip install dash`
- **Pandas**: `pip install pandas`
- **Plotly**: `pip install plotly`
- **pymongo**: `pip install pymongo`

MongoDB should be installed and running on your system to store and query the dataset.

## Dataset

The dataset used for this project was sourced from [Kaggle: Remote Work and Mental Health](https://www.kaggle.com/datasets/waqi786/remote-work-and-mental-health). It contains information on 5,000 employees, including their work location, mental health conditions, stress levels, and productivity changes.

### Dataset Attributes

- **Employee_ID**: Unique identifier for each employee.
- **Age**, **Gender**, **Job_Role**, **Industry**: Demographic data.
- **Work_Location**: Type of work location (Remote, Onsite, Hybrid).
- **Work_Life_Balance_Rating**: Rating of work-life balance (1 to 5 scale).
- **Stress_Level**: Categorical variable indicating employee stress levels (Low, Medium, High).
- **Mental_Health_Condition**: Information on any mental health conditions (Anxiety, Depression, None).
- **Productivity_Change**: How the employee's productivity changed due to work location (Increase, Decrease, No Change).

## Running the Project

### Step 1: Install Dependencies
First, install the necessary Python packages using `pip`:
```bash
pip install flask dash pandas plotly pymongo



 
