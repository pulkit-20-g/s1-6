import csv
import xml.etree.ElementTree as ET

def parse_pos_file(pos_filename):
    """
    Parse the .pos file to extract relevant columns and clean the data.
    
    Args:
        pos_filename (str): The path to the input .pos file.
    
    Returns:
        list of dict: List of cleaned data rows.
    """
    pos_data = []
    
    with open(pos_filename, 'r') as pos_file:
        lines = pos_file.readlines()
        for line in lines:
            # Skip comment or non-data lines
            if line.startswith('%'):
                continue
            # Split the line into values
            parts = line.split()
            if len(parts) >= 12:  # Ensure we have enough data fields
                latitude = parts[2]
                longitude = parts[3]
                height = parts[4]
                quality = parts[5]
                ns = parts[6]
                sdn = parts[7]
                sde = parts[8]
                # Store the cleaned data
                pos_data.append({
                    'latitude': latitude,
                    'longitude': longitude,
                    'height': height,
                    'Q': quality,
                    'ns': ns,
                    'sdn': sdn,
                    'sde': sde
                })
    return pos_data


def parse_kml_file(kml_filename):
    """
    Parse the .kml file to extract relevant KML data (coordinates).
    
    Args:
        kml_filename (str): The path to the input .kml file.
    
    Returns:
        list of dict: List of cleaned KML data rows.
    """
    kml_data = []
    
    tree = ET.parse(kml_filename)
    root = tree.getroot()
    
    # Define namespaces for XML parsing
    namespaces = {'kml': 'http://earth.google.com/kml/2.1'}
    
    # Extract all Placemark elements (assuming data is within these elements)
    for placemark in root.findall('.//kml:Placemark', namespaces):
        coordinates = placemark.find('.//kml:coordinates', namespaces)
        if coordinates is not None:
            coord_str = coordinates.text.strip()
            coords = coord_str.split(',')
            if len(coords) >= 2:
                latitude = coords[1]
                longitude = coords[0]
               
                
                kml_data.append({
                    'latitude': latitude,
                    'longitude': longitude
                })
    return kml_data


def write_to_csv(data, filename, headers):
    """
    Write cleaned data to a CSV file.
    
    Args:
        data (list of dict): The data to write.
        filename (str): The name of the output CSV file.
        headers (list of str): The CSV header row.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():
    # Input file paths from the user
    pos_filename = input("Enter the path of the .pos file: ")
    kml_filename = input("Enter the path of the .kml file: ")
    
    # Parse the .pos and .kml files
    pos_data = parse_pos_file(pos_filename)
    kml_data = parse_kml_file(kml_filename)
    
    # Output CSV file paths
    pos_output_filename = 'cleaned_pos_data.csv'
    kml_output_filename = 'cleaned_kml_data.csv'
    
    # Define the headers for the CSV files
    pos_headers = ['latitude', 'longitude', 'height', 'Q', 'ns', 'sdn', 'sde']
    kml_headers = ['latitude', 'longitude']
    
    # Write cleaned data to CSV
    write_to_csv(pos_data, pos_output_filename, pos_headers)
    write_to_csv(kml_data, kml_output_filename, kml_headers)
    
    print(f"Cleaned data from .pos file written to {pos_output_filename}")
    print(f"Cleaned data from .kml file written to {kml_output_filename}")


if __name__ == '__main__':
    main()
    print("hello world")

