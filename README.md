# DSCI 510 Final Project - Analyzing California Wildfires: Patterns, Trends, and Insights
California wildfires have become increasingly devastating over the past decade, with far-reaching impacts on ecosystems, communities, and economies. The purpose of this project is to understand the underlying trends and patterns of wildfire incidents to gain actionable insights into their causes, behavior, and management effectiveness.

This project focuses on analyzing California wildfire data from 2015 to 2024 to identify trends and patterns in wildfire activity. The dataset includes information such as fire names, start and extinguished dates, acres burned, and location data. By visualizing and analyzing these metrics, this project aims to provide insights into wildfire behavior, identify high-risk regions, and assess the effectiveness of containment efforts.

The California wildfire incident data is collected from [The California Department of Forestry and Fire Protection](https://www.fire.ca.gov/incidents).

## Create a Conda Enviornment
```bash
conda create --name env_name python=3.9
```

## Install the Required Libraries
Make sure all required Python libraries are installed. Run the following command to install dependencies: 
```bash
pip install -r requirements.txt
```

## Download the Raw Data
Run the following script to download the raw wildfire incidents data to the data/raw folder:  
```bash
python get_data.py
```

## Clean the Data
The raw dataset may contain missing/invalid/irrelevant data for data analysis. Run the following script to clean and preprocess the dataset:  
```bash
python clean_data.py
```

## Run Analysis and Visualizations
Perform data analysis by running the analysis script:  
```bash
python analyze_visualize_results.py
```
