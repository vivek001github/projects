import streamlit as st
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from geopy.distance import geodesic
import matplotlib.pyplot as plt
from datetime import timedelta
import numpy as np
import time
import math

# Function to create the data model
def create_data_model():
    data = {}
    data["locations"] = [
        (12.9662442, 77.606641),  # Lalbagh Botanical Garden (Start/Depot)
        (12.874145, 77.632046),   # Bommanahalli
        (13.0357703, 77.5970225), # Manyata Tech Park
        (12.9028005, 77.6082448), # HSR Layout
        (12.9279232, 77.6271078), # M.G. Road
        (12.8237803, 77.6649865), # Electronic City
        (13.0117002, 77.5547754), # Yeshwanthpur
        (12.954517, 77.350736),   # Bannerghatta National Park
        (12.9351929, 77.6244807), # Koramangala
        (12.9717201, 77.6027821), # Cubbon Park
        (12.9718915, 77.6411545), # Indiranagar
        (12.974442, 77.580643),   # Vidhana Soudha
        (12.926031, 77.676246),   # Sarjapur
        (12.9345334, 77.626579),  # Jayanagar
        (13.0081, 77.5696),       # Mathikere
        (13.0227134, 77.5969603)  # Hebbal (End)
    ]
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data

# Function to compute distance between two locations
def compute_distance(location1, location2):
    return geodesic(location1, location2).meters

# Function to calculate total time spent in a day
def calculate_daily_time(travel_distance, task_time_per_location, break_time, lunch_break):
    total_travel_time = travel_distance / 50000  # Assume avg speed 50 km/h
    total_task_time = task_time_per_location
    return total_travel_time + total_task_time + break_time + lunch_break

# Function to print the solution and generate daily itineraries
def print_solution(data, manager, routing, solution, task_time=10, break_time=30, lunch_break=45, hours_per_day=8):
    route_distance = 0
    route = []
    total_days = []
    day_time_limit = hours_per_day * 60  # Total minutes per day
    total_time = 0
    task_time_total = task_time * len(data["locations"])

    day_route = []
    current_day_time = 0

    index = routing.Start(0)  # Only one vehicle (vehicle_id = 0)

    while not routing.IsEnd(index):
        node_index = manager.IndexToNode(index)
        route.append(data["locations"][node_index])
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        distance_between_points = routing.GetArcCostForVehicle(previous_index, index, 0) / 1000  # Convert to kilometers
        travel_time = (distance_between_points / 50) * 60  # Travel time in minutes (assuming 50 km/h avg)
        
        current_day_time += travel_time + task_time  # Adding travel and task time

        # Adding breaks and lunch
        if current_day_time >= 240:  # Mid-day break at 4 hours (240 mins)
            current_day_time += break_time
        if current_day_time >= 360:  # Lunch break after 6 hours (360 mins)
            current_day_time += lunch_break

        # Check if the daily limit is exceeded
        if current_day_time > day_time_limit:
            total_days.append(day_route)  # Add the route for the day
            day_route = []  # Start a new day
            current_day_time = 0  # Reset time for the next day
        
        day_route.append(data["locations"][node_index])
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    
    total_days.append(day_route)  # Add the last day's route
    return total_days, route_distance

# Function to plot the route
def plot_route_with_arrows(route, day_number):
    fig, ax = plt.subplots(figsize=(10, 8))
    latitudes, longitudes = zip(*route)
    
    for i in range(len(route) - 1):
        ax.arrow(longitudes[i], latitudes[i], 
                 longitudes[i + 1] - longitudes[i], 
                 latitudes[i + 1] - latitudes[i], 
                 head_width=0.0005, color='blue', length_includes_head=True)

    ax.scatter(longitudes, latitudes, marker='o', color='red', s=100, zorder=5)
    
    for i, (lat, long) in enumerate(route):
        ax.text(long, lat, f"Day {day_number}: {i}", fontsize=12, ha='right', va='bottom', color='black')

    depot_lat, depot_long = route[0]
    ax.scatter([depot_long], [depot_lat], c='green', s=150, label='Depot', zorder=6)
    
    ax.set_title(f'Travel Route for Day {day_number}')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.grid(True)
    
    st.pyplot(fig)

# Main function for Streamlit app
def main():
    st.title("Multi-Day Location Routing Problem")

    st.sidebar.header("Configuration")
    
    # Allow user to set max distance
    max_distance = st.sidebar.slider("Max Vehicle Travel Distance (meters)", 1000000, 50000000, 20000000)
    
    # Data model
    data = create_data_model()
    
    # Create routing index manager
    manager = pywrapcp.RoutingIndexManager(len(data["locations"]), data["num_vehicles"], data["depot"])
    
    # Create Routing Model
    routing = pywrapcp.RoutingModel(manager)
    
    # Create and register a transit callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(compute_distance(data["locations"][from_node], data["locations"][to_node]))
    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
    # Add Distance constraint
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        max_distance,  # max travel distance
        True,  # start cumul to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)
    
    # Set first solution heuristic
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    
    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)
    
    if solution:
        # Print and plot solution
        task_time = 10  # Time spent at each location in minutes
        break_time = 30  # Two 15 minute breaks
        lunch_break = 45  # Lunch break of 45 minutes
        hours_per_day = 8  # Total work hours per day
        
        total_days, route_distance = print_solution(data, manager, routing, solution, task_time, break_time, lunch_break, hours_per_day)
        
        st.subheader(f"Total Route Distance: {route_distance / 1000:.2f} kilometers")
        
        for day_number, day_route in enumerate(total_days, 1):
            st.subheader(f"Day {day_number} Route:")
            st.write(f"Number of locations: {len(day_route)}")
            plot_route_with_arrows(day_route, day_number)
    else:
        st.error("No solution found!")

# Run the Streamlit app
if __name__ == "__main__":
    main()
