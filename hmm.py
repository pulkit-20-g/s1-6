!pip install hmmlearn
!pip install folium
import numpy as np
import pandas as pd
from hmmlearn import hmm
import folium

# Set the random seed for reproducibility
np.random.seed(42)  # Use any integer you want for a fixed seed

# Load your snapped data
snapped_data = pd.read_csv('snapped_points.csv')

# Prepare the coordinates (latitude, longitude) as the feature vector for HMM
coordinates = snapped_data[['latitude', 'longitude']].values

# Define the HMM model (assuming two road types: highway and service road)
model = hmm.GaussianHMM(n_components=2, covariance_type="diag", n_iter=1000, random_state=42)

# Train the model on the snapped coordinates
model.fit(coordinates)

# Predict the road types (hidden states) based on the coordinates
predicted_states = model.predict(coordinates)

# Map the predicted states back to road types (0: highway, 1: service road)
reverse_state_map = {0: 'highway', 1: 'service_road'}
predicted_road_types = [reverse_state_map[state] for state in predicted_states]

# Add the predicted road types to the original data
snapped_data['predicted_road_type'] = predicted_road_types

# Now, we will plot the results on OpenStreetMap
map_center = [snapped_data['latitude'].mean(), snapped_data['longitude'].mean()]
osm_map = folium.Map(location=map_center, zoom_start=15)

# Add markers to the map based on the predicted road type
for _, row in snapped_data.iterrows():
    color = 'blue' if row['predicted_road_type'] == 'highway' else 'green'
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Road Type: {row['predicted_road_type']}",
        icon=folium.Icon(color=color)
    ).add_to(osm_map)

# Save the map to an HTML file for viewing
osm_map.save('osm_map_hmm.html')

print("HMM classification and map generation complete!")
