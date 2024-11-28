import pandas as pd
import folium
from folium.plugins import MarkerCluster

def load_csv_data(csv_filename):
    """
    Load GPS data from a CSV file.
    
    Args:
        csv_filename (str): The path to the input CSV file.
    
    Returns:
        DataFrame: A Pandas DataFrame containing the data from the CSV.
    """
    return pd.read_csv(csv_filename)

def create_map():
    """
    Create an initial OpenStreetMap centered at a default location.
    
    Returns:
        folium.Map: The Folium map object.
    """
    # You can change this location to any coordinate you want to start with.
    map_center = [37.7749, -122.4194]  # San Francisco coordinates as an example
    return folium.Map(location=map_center, zoom_start=12)

def plot_gps_points_on_map(data, map_obj):
    """
    Plot GPS data points on the OpenStreetMap.
    
    Args:
        data (DataFrame): The GPS data as a DataFrame.
        map_obj (folium.Map): The Folium map object to plot on.
    """
    # Create a MarkerCluster to group markers when zoomed out
    marker_cluster = MarkerCluster().add_to(map_obj)

    # Iterate through each row of the data and add a marker
    for _, row in data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Latitude: {row['latitude']}, Longitude: {row['longitude']}"
        ).add_to(marker_cluster)

def save_map(map_obj, filename='osm_map.html'):
    """
    Save the map as an HTML file.
    
    Args:
        map_obj (folium.Map): The Folium map object to save.
        filename (str): The name of the output HTML file.
    """
    map_obj.save(filename)

def main():
    # Load the cleaned GPS data from the CSV files
    pos_data = load_csv_data('/Users/pulkitgarg/Desktop/SIH/snapped_points.csv')
    # kml_data = load_csv_data('cleaned_kml_data.csv')

    # Create a new OpenStreetMap
    osm_map = create_map()

    # Plot both datasets on the map
    plot_gps_points_on_map(pos_data, osm_map)
    # plot_gps_points_on_map(kml_data, osm_map)

    # Save the map to an HTML file
    save_map(osm_map, 'osm_map.html')

    print("The map has been generated and saved as 'osm_map.html'. You can open it in your browser.")

if __name__ == '__main__':
    main()
