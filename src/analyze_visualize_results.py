import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from pandas import DataFrame

def fire_incidents_map(fire_data: DataFrame):
    """
    Build a map that shows the location of the California wildfire incidents and
    Save it to the results/visualizations folder

    Args:
        fire_data (DataFrame): The input DataFrame
    """
    fire_loc = fire_data[(fire_data['Longitude'] != 0) & (fire_data['Latitude'] != 0)]
    valid_fire_data = fire_loc[
        (fire_loc['Latitude'] >= 32) & (fire_loc['Latitude'] <= 42) &
        (fire_loc['Longitude'] >= -124) & (fire_loc['Longitude'] <= -114)]

    center_lat = valid_fire_data['Latitude'].mean()
    center_lon = valid_fire_data['Longitude'].mean()

    fire_map = folium.Map(location=[center_lat, center_lon], zoom_start=6)

    for _, row in valid_fire_data.iterrows():
        popup_info = f"""
        <b>Fire Name:</b> {row['Name']}<br>
        <b>County:</b> {row['County']}<br>
        <b>Acres Burned:</b> {row['AcresBurned']}<br>
        <b>Percent Contained:</b> {row['PercentContained']}<br>
        <b>Started:</b> {row['Started']}<br>
        <b>Extinguished Time:</b> {row['ExtinguishedTime']}
        """
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=3,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.7,
            popup=folium.Popup(popup_info, max_width=300),
        ).add_to(fire_map)

    output_folder = '../results/visualizations'
    os.makedirs(output_folder, exist_ok=True)

    # Save the map to the specified folder
    output_file_path = os.path.join(output_folder, 'fire_location_map.html')
    fire_map.save(output_file_path)

def incidents_by_year(fire_data: DataFrame):
    """
    Visualize fire incidents by year,
    Show the bar plot, and
    Save it to the results/visualizations folder

    Args:
        fire_data (DataFrame): The input DataFrame
    """
    mean_value = fire_data['Year'].value_counts().mean()
    sns.countplot(x=fire_data['Year'])
    plt.title('Number of Fire Incidents from 2015 to 2024')
    plt.ylabel('Number of Incidents')
    plt.axhline(y=mean_value, color='r', linestyle='--', label='Mean')
    plt.legend()
    plt.show()

    folder_path = '../results/visualizations'
    os.makedirs(folder_path, exist_ok=True)
    pdf_path = os.path.join(folder_path, 'fire_incidents_plot.pdf')
    plt.savefig(pdf_path, format='pdf')
    plt.close()

def top_incidents_acre_burned(fire_data: DataFrame, top: int = 10):
    """
    Visualize top 10 counties with the most number of incidents and total acres burned,
    Show the bar plot, and
    Save it to the results/visualizations folder

    Args:
        fire_data (DataFrame): The input DataFrame
        top (int): The rank, default 10
    """
    county_summary = fire_data.groupby('County').agg({
        'Name': 'count', 'AcresBurned': ['sum', 'mean']}).reset_index()
    county_summary.columns = ['County', 'TotalFires', 'TotalAcresBurned', 'AvgAcresBurned']

    # Top 10 counties by Total Fires
    total_fire_summary = county_summary.sort_values('TotalFires', ascending=False)[:top]

    # Top 10 counties by Total Acres Burned
    acre_burned_summary = county_summary.sort_values('TotalAcresBurned', ascending=False)[:top]

    plt.figure(figsize=(12, 6))

    # Subplot 1: Total Fires by County
    plt.subplot(1, 2, 1)
    plt.bar(total_fire_summary['County'], total_fire_summary['TotalFires'])
    plt.xticks(rotation=45)
    plt.xlabel('County')
    plt.ylabel('Total Fires')
    plt.title('Total Fires by County')

    # Subplot 2: Total Acres Burned by County
    plt.subplot(1, 2, 2)
    plt.bar(acre_burned_summary['County'], acre_burned_summary['TotalAcresBurned'])
    plt.xticks(rotation=45)
    plt.xlabel('County')
    plt.ylabel('Total Acres Burned')
    plt.title('Total Acres Burned by County')
    plt.tight_layout()
    plt.show()

    folder_path = '../results/visualizations'
    os.makedirs(folder_path, exist_ok=True)
    pdf_path = os.path.join(folder_path, 'top_num_fire_total_acre.pdf')
    plt.savefig(pdf_path, format='pdf')
    plt.close()

def containment_over_time(fire_data: DataFrame):
    """
    Visualize fire containment over time,
    Show the line plot, and
    Save it to the results/visualizations folder

    Args:
        fire_data (DataFrame): The input DataFrame
    """
    fire_data['Year'] = pd.to_datetime(fire_data['Started'], errors='coerce').dt.year
    containment_by_year = fire_data.groupby('Year')['PercentContained'].mean()

    plt.plot(containment_by_year.index, containment_by_year.values)
    plt.xlabel('Year')
    plt.ylabel('Average Percent Contained')
    plt.title('Trends in Fire Containment over Time')
    plt.show()

    folder_path = '../results/visualizations'
    os.makedirs(folder_path, exist_ok=True)
    pdf_path = os.path.join(folder_path, 'containment_over_time.pdf')
    plt.savefig(pdf_path, format='pdf')
    plt.close()

def top_10_extinguishment_time(fire_data: DataFrame, top: int = 10):
    """
    Visualize top 10 counties with the longest extinguishment time,
    Show the bar plot, and
    Save it to the results/visualizations folder

    Args:
        fire_data (DataFrame): The input DataFrame
        top (int): The rank, default 10
    """
    top_counties = fire_data.groupby('County')['ExtinguishedTime'].mean().nlargest(10)

    sns.barplot(x=top_counties.values, y=top_counties.index)
    plt.xlabel('Average Extinguishment Time (hours)')
    plt.ylabel('County')
    plt.title('Top 10 Counties with Longest Extinguishment Time')
    plt.show()

    folder_path = '../results/visualizations'
    os.makedirs(folder_path, exist_ok=True)
    pdf_path = os.path.join(folder_path, 'extinguishment_time.pdf')
    plt.savefig(pdf_path, format='pdf')
    plt.close()

def avg_time_by_county_year(fire_data: DataFrame):
    """
    Visualize top 10 counties with the longest extinguishment time,
    Show the heatmap, and
    Save it to the results/visualizations folder

    Args:
        fire_data (DataFrame): The input DataFrame
    """
    pivot_table = fire_data.pivot_table(values='ExtinguishedTime', index='County', columns='Year', aggfunc='mean')

    plt.figure(figsize=(12, 12))
    sns.heatmap(pivot_table, cmap='coolwarm', annot=True, fmt=".1f", linewidths=0.3)
    plt.title('Average Extinguishment Time by County and Year')
    plt.xlabel('Year')
    plt.ylabel('County')
    plt.show()

    folder_path = '../results/visualizations'
    os.makedirs(folder_path, exist_ok=True)
    pdf_path = os.path.join(folder_path, 'avg_time_by_county_year.pdf')
    plt.savefig(pdf_path, format='pdf')
    plt.close()

if __name__ == '__main__':
    fire_data = pd.read_csv('../data/processed/fire_incidents_data.csv')
    fire_incidents_map(fire_data)
    incidents_by_year(fire_data)
    top_incidents_acre_burned(fire_data)
    containment_over_time(fire_data)
    top_10_extinguishment_time(fire_data)
    avg_time_by_county_year(fire_data)
