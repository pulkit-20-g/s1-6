import pandas as pd
import folium

# Function to plot latitude, longitude from CSV and save map as HTML
def plot_lat_lon_on_osm(csv_file, output_html='map.html'):
    # Step 1: Load the CSV file containing latitude and longitude
    try:
        data = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: The file {csv_file} does not exist.")
        return

    # Step 2: Check if the necessary columns exist
    if 'latitude' not in data.columns or 'longitude' not in data.columns:
        print("Error: CSV file must contain 'latitude' and 'longitude' columns.")
        return

    # Step 3: Create a base map centered on the average latitude and longitude
    map_center = [data['latitude'].mean(), data['longitude'].mean()]
    osm_map = folium.Map(location=map_center, zoom_start=12)

    # Step 4: Add points to the map
    for _, row in data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Lat: {row['latitude']}, Lon: {row['longitude']}",
            icon=folium.Icon(color='red')
        ).add_to(osm_map)

    # Step 5: Save the map to an HTML file
    osm_map.save(output_html)
    print(f"Map has been saved to {output_html}")

# Example usage:
csv_file = '/Users/pulkitgarg/Desktop/SIH/snapped_points_3.csv'  # Replace with your CSV file path
output_html = 'output_map.html'  # Output HTML file
plot_lat_lon_on_osm(csv_file, output_html)
