import csv
import requests

# Function to snap a point to the nearest road using OSRM's Nearest API
def snap_to_road(lat, lon):
    osrm_url = f'http://router.project-osrm.org/nearest/v1/driving/{lon},{lat}'
    response = requests.get(osrm_url)
    if response.status_code == 200:
        data = response.json()
        # Extract the snapped point's coordinates (lat, lon)
        snapped_point = data['waypoints'][0]['location']
        snapped_lat = snapped_point[1]
        snapped_lon = snapped_point[0]
        return snapped_lat, snapped_lon
    else:
        print(f"Error with request: {response.status_code}")
        return None, None

# Function to process the CSV file and snap all points to the nearest road
def process_gnss_csv(input_csv, output_csv):
    with open(input_csv, mode='r') as infile, open(output_csv, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = [ 'snapped_latitude', 'snapped_longitude']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()

        for row in reader:
            lat = float(row['latitude'])
            lon = float(row['longitude'])
            snapped_lat, snapped_lon = snap_to_road(lat, lon)
            
            if snapped_lat is not None and snapped_lon is not None:
                writer.writerow({
                    # 'latitude': lat,
                    # 'longitude': lon,
                    'snapped_latitude': snapped_lat,
                    'snapped_longitude': snapped_lon
                })

# Input and output CSV file paths
input_csv = '/Users/pulkitgarg/Desktop/SIH/python/cleaned_kml_data.csv'
output_csv = 'snapped_points.csv'

# Process the GNSS points and snap them to the nearest road
process_gnss_csv(input_csv, output_csv)

