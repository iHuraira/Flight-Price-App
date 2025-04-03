import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import gaussian_kde
import numpy as np
import plotly.graph_objects as go
import random
import plotly.colors as pc 

# Title
st.title('Dashboard Overview')

# Description
st.write("""
Welcome to the interactive dashboard! Here, you can explore various aspects of the data, analyze trends, and visualize key insights.
""")

@st.cache_data
def load_data(path):    
 return pd.read_csv(path)

data = load_data("artifacts/Data/Preprocessed.csv")

selected_columns = st.multiselect(options=data.columns, label="select")

st.write(f"Dataset Dimensions {data.shape}")

if len(selected_columns) == 0:
    st.write("Showing full data:")
    st.write(data.head(5))
else:
    st.write(f"Showing selected columns: {', '.join(selected_columns)}")
    st.write(data[selected_columns].head(5))


category_columns = ['airline_name', 'departure_city', 'arrival_city', 'flight_type', 'departure_time_of_day', 'arrival_time_of_day',
'flight_code_category']

# Create two columns in Streamlit (adjusted for your request to have 2 columns)
col1, col2 = st.columns(2)

# Create a selectbox in the first column for selecting the column to analyze for frequency
with col1:
    column_to_analyze = st.selectbox("Select a column to analyze the frequency of categories", options=category_columns)

# Check if a valid column is selected and plot the frequency in the first column
if column_to_analyze:
    with col1:
        # Count the frequency of each unique value in the selected column
        category_counts = data[column_to_analyze].value_counts().reset_index()
        category_counts.columns = [column_to_analyze, 'Frequency']
        
        # Create a bar plot with Plotly Express
        fig = px.bar(category_counts, 
                     x=column_to_analyze, 
                     y='Frequency', 
                     labels={column_to_analyze: column_to_analyze, 'Frequency': 'Count'},
                     color=column_to_analyze)
        
        # Display the plot in the first column
        st.plotly_chart(fig)

# Create a KDE plot with bars in the second column
@st.cache_data  # Cache the function for faster repeated access
def compute_kde_and_histogram(data_values, num_points=200, bins=30):
    # Compute the KDE (Kernel Density Estimate) using SciPy's gaussian_kde
    kde = gaussian_kde(data_values)
    
    # Generate a range of values for the X-axis for plotting
    x_range = np.linspace(min(data_values), max(data_values), num_points)
    y_range = kde(x_range)
    
    # Compute histogram for the data
    hist, bin_edges = np.histogram(data_values, bins=bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    return x_range, y_range, hist, bin_centers

with col2:
    # Select a numerical column for the KDE plot
    numeric_column = st.selectbox("Select a numerical column to plot KDE with bars", options=['ticket_price', 'flight_duration_minutes',
       'delay_duration_minutes'])
    
    if numeric_column:
        # Remove missing values
        data_values = data[numeric_column].dropna()
        
        # Reduce the number of points evaluated for the KDE
        num_points = 400  # You can experiment with 100, 200, or 300
        bins = 40  # Number of bins for the histogram
        
        # Compute KDE and histogram with caching to speed up subsequent calls
        x_range, y_range, hist, bin_centers = compute_kde_and_histogram(data_values, num_points, bins)
        
        # Create the plot with both the KDE and the histogram bars
        fig_kde_bars = go.Figure()

        # Add the histogram bars with vibrant colors and a custom outline
        fig_kde_bars.add_trace(go.Bar(
            x=bin_centers,
            y=hist,
            name="Histogram",
            marker=dict(color='#98D8EF'),  # Bright orange
            hoverinfo='x+y',
            opacity=1
        ))

        # Set the layout for the figure
        fig_kde_bars.update_layout(
            xaxis_title=numeric_column,
            yaxis_title='Density',
            template="plotly",  # Clean template to allow colors to shine
            xaxis=dict(
                showgrid=True,
                zeroline=False,
                showline=True,
                linecolor='#F2EFE7',  # White axis line for contrast
            ),
            yaxis=dict(
                showgrid=True,
                zeroline=False,
                showline=True,
                linecolor='#F2EFE7'  # White axis line for contrast
            ),
            
            hovermode="closest",  # Enhance hover experience
        )

        # Display the colorful plot in the second column
        st.plotly_chart(fig_kde_bars)

    

import plotly.graph_objects as go

# Define the list of columns for which we want to create donut plots
columns_to_plot = ['num_stops', 'is_late', 'is_overnight', 'is_early', 'is_frequent_route', 'is_rare_flight']

st.markdown("""
### Flight Characteristics Overview

Flight characteristics significantly influence travel convenience. Here's a quick look at some key attributes:

- **Number of Stops**: Non-stop flights are generally faster and more convenient, while flights with multiple stops can be cheaper but take longer.

- **Flight Delays**: Delays affect travel time. Understanding common delay patterns helps travelers choose better routes and avoid disruptions.

- **Overnight Flights**: These flights depart late and arrive the next morning, offering convenience for time-sensitive travelers but may disrupt sleep.

- **Early Flights**: Early departures are often on-time and less crowded, ideal for travelers seeking efficiency.

- **Frequent Routes**: Popular routes with high demand offer flexibility in scheduling and often better prices.

- **Rare Flights**: Less frequent routes between smaller destinations may have higher ticket prices and limited availability.
""")


# Create a row with 6 columns
col1, col2, col3, col4, col5, col6 = st.columns(6)

# List of columns and corresponding column containers
columns = [col1, col2, col3, col4, col5, col6]

# Function to map 1 and 0 to "Yes" and "No"
def map_yes_no(value):
    return "Yes" if value == 1 else "No"

# Custom names for display (remove 'is_' and capitalize first letter)
column_display_names = {
    'num_stops': 'Stops',
    'is_late': 'Late',
    'is_overnight': 'Overnight',
    'is_early': 'Early',
    'is_frequent_route': 'Frequent Route',
    'is_rare_flight': 'Rare Flight'
}

# Loop through the columns to create the donut plots
for idx, column in enumerate(columns_to_plot):
    # Count the frequency of each unique value in the column
    column_counts = data[column].value_counts().reset_index()
    column_counts.columns = [column, 'Frequency']

    # If the column contains binary values (like 1 and 0), map them to "Yes" and "No"
    if column in ['is_late', 'is_overnight', 'is_early', 'is_frequent_route', 'is_rare_flight']:
        column_counts[column] = column_counts[column].map(map_yes_no)
    
    # Create the donut plot (pie chart with hole in the center)
    fig = go.Figure(go.Pie(
        labels=column_counts[column],
        values=column_counts['Frequency'],
        hole=0.7,  # Makes it a donut plot
        hoverinfo='label+percent',
        textinfo='percent+label',
        marker=dict(colors=['#FF6347', '#4682B4']),  # Choose colors (can be customized)
    ))

    # Update the layout for better visuals
    fig.update_layout(
        title=f"{column_display_names[column]}",  # Use custom name
        title_x=0.36,
        showlegend=False,
        template="plotly_dark",  # Optional: change to a dark template
        width=300,  # Fixed width for each donut plot
        height=300,  # Fixed height for each donut plot
    )

    # Display each donut plot in the respective column
    with columns[idx]:
        st.plotly_chart(fig)


# Create a container for the donut plots
st.markdown("## Flight Network")

# City coordinates dictionary
city_coordinates = {
    "Delhi": {"latitude": 28.6139, "longitude": 77.2090},
    "Mumbai": {"latitude": 19.0760, "longitude": 72.8777},
    "Bangalore": {"latitude": 12.9716, "longitude": 77.5946},
    "Kolkata": {"latitude": 22.5726, "longitude": 88.3639},
    "Chennai": {"latitude": 13.0827, "longitude": 80.2707},
    "Hyderabad": {"latitude": 17.3850, "longitude": 78.4867}
}

# Calculate flight count based on the occurrence of each departure and arrival city pair
flight_counts = data.groupby(['departure_city', 'arrival_city']).size().reset_index(name='flight_count')

# Prepare a list of lines (routes) and their thickness
routes = []

# Get the Magma color scale (dividing it into as many colors as routes)
magma_colors = pc.sample_colorscale('magma', len(flight_counts))  # Generate a color list based on Magma scale

for idx, row in flight_counts.iterrows():
    departure = row['departure_city']
    arrival = row['arrival_city']
    flight_count = row['flight_count']
    
    # Get coordinates of departure and arrival cities
    departure_coords = city_coordinates[departure]
    arrival_coords = city_coordinates[arrival]
    
    # Append the route and its corresponding flight count and color
    routes.append({
        "departure_city": departure,
        "arrival_city": arrival,
        "departure_lat": departure_coords["latitude"],
        "departure_lon": departure_coords["longitude"],
        "arrival_lat": arrival_coords["latitude"],
        "arrival_lon": arrival_coords["longitude"],
        "flight_count": flight_count,
        "color": magma_colors[idx]  # Assign color from the Magma scale
    })

# Create a map with lines for the routes
fig = go.Figure()

# Add each route as a line
for route in routes:
    # Scale down the flight count for line width
    line_width = route["flight_count"] / 2000  # Adjust the divisor to scale better
    if line_width < 1:
        line_width = 1  # Ensure that lines don't become too thin
    
    fig.add_trace(go.Scattermapbox(
        mode="lines",
        lon=[route["departure_lon"], route["arrival_lon"]],
        lat=[route["departure_lat"], route["arrival_lat"]],
        line=dict(width=line_width, color=route["color"]),  # Assign color for each route
        hoverinfo="text",
        text=f"{route['arrival_city']}<br>{route['departure_city']}",  # Tooltip format
        showlegend=False  # Remove the legend for these routes
    ))

# Add the cities as points (optional)
city_data = []
for city, coords in city_coordinates.items():
    city_data.append({
        "city": city,
        "latitude": coords["latitude"],
        "longitude": coords["longitude"]
    })

# Add points for each city
for city in city_data:
    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lon=[city["longitude"]],
        lat=[city["latitude"]],
        marker=dict(size=10, color="red"),
        hoverinfo="text",
        text=city["city"],
        showlegend=False  # Remove legend for city markers
    ))

# Update layout settings for the map
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=5,  # Adjust zoom level
    mapbox_center={"lat": 20.5937, "lon": 78.9629},  # Center of India
    height=800,  # Adjust map height
    width=500,   # Adjust map width
    mapbox=dict(
        zoom=5,  # Initial zoom level
        center={"lat": 20.5937, "lon": 78.9629},  # Center map on India
        style="carto-positron",  # Map style
        accesstoken="your-mapbox-access-token-here",  # Optional if using custom Mapbox token
    )
)

# Display the map in Streamlit
st.plotly_chart(fig)

footer = """
<style>
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #f1f1f1;
    color: #000;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    border-top: 1px solid #e1e1e1;
}
</style>
<div class="footer">
    ⏱️ Built with ❤️ using Streamlit | © 2025 Your Name or Company
</div>
"""

st.markdown(footer, unsafe_allow_html=True)