import streamlit as st
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import numpy as np

# Function to create the data model
def create_data_model():
    data = {}
    data["locations"] = [
        (12.9662442, 77.606641),  # Lalbagh Botanical Garden (Depot)
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
        (13.0227134, 77.5969603)  # Hebbal
    ]
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data

# Function to compute distance between two locations
def compute_distance(location1, location2):
    return geodesic(location1, location2).meters

# Function to plot the route
def plot_route_with_arrows(route):
    fig, ax = plt.subplots(figsize=(10, 8))
    latitudes, longitudes = zip(*route)
    
    for i in range(len(route) - 1):
        ax.arrow(longitudes[i], latitudes[i], 
                 longitudes[i + 1] - longitudes[i], 
                 latitudes[i + 1] - latitudes[i], 
                 head_width=0.0005, color='blue', length_includes_head=True)

    ax.scatter(longitudes, latitudes, marker='o', color='red', s=100, zorder=5)
    
    for i, (lat, long) in enumerate(route):
        ax.text(long, lat, str(i), fontsize=12, ha='right', va='bottom', color='black')

    depot_lat, depot_long = route[0]
    ax.scatter([depot_long], [depot_lat], c='green', s=150, label='Depot', zorder=6)
    
    ax.set_title('Travel Route with Arrows Indicating Direction')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.grid(True)
    
    st.pyplot(fig)

# Function to print the solution
def print_solution(data, manager, routing, solution):
    route_distance = 0
    route = []
    index = routing.Start(0)  # Only one vehicle (vehicle_id = 0)
    
    while not routing.IsEnd(index):
        node_index = manager.IndexToNode(index)
        route.append(data["locations"][node_index])
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    
    route.append(data["locations"][manager.IndexToNode(index)])  # End node
    return route, route_distance

# Main function for Streamlit app
def main():
    st.title("Vehicle Routing Problem")

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
        route, route_distance = print_solution(data, manager, routing, solution)
        
        st.subheader(f"Route Distance: {route_distance} meters")
        
        plot_route_with_arrows(route)
        
        # Show the solution as text
        st.subheader("Route:")
        route_str = " -> ".join([f"{i}" for i in range(len(route))])
        st.write(route_str)
    else:
        st.error("No solution found!")

# Run the Streamlit app
if __name__ == "__main__":
    main()
