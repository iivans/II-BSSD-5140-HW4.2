import requests
import math
import heapq  # We will use heap for Dijkstra's algorithm

URL_PATH = "https://nominatim.openstreetmap.org/search"

# THIS GETS LOCATION
def get_lat_lon(location):
    PARAMS = {'q': location, 'format': 'jsonv2'}
    headers = {'User-Agent': 'DistanceCalc/1.0'}
    response = requests.get(URL_PATH, params=PARAMS, headers=headers)
    data = response.json()
    return [float(data[0]['lat']), float(data[0]['lon'])]

# THIS CALCULATES DISTANCE 
def calculate_distance(lat1, lon1, lat2, lon2):
    dlon = math.radians(lon2 - lon1)
    dlat = math.radians(lat2 - lat1)
    a = (math.sin(dlat/2))**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (math.sin(dlon/2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = 3961 * c  # Radius of Earth in miles
    return d

# DIJKSTRA'S ALGORITHM
def dijkstra(graph, start, goal):
    # Priority queue to store (distance, node)
    queue = [(0, start)]
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    path = {node: None for node in graph}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        # If we reach the goal node, stop
        if current_node == goal:
            break

        if current_distance > distances[current_node]:
            continue

        # Explore neighbors
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # Only consider this new path if it's better
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                path[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # Reconstruct the shortest path
    final_path = []
    current_node = goal
    while current_node:
        final_path.append(current_node)
        current_node = path[current_node]
    
    return final_path[::-1], distances[goal]

# MAIN PROGRAM
def main():
    cities = [
        "Gilroy, CA",
        "Cheyenne, WY",
        "Fargo, ND",
        "Zanesville, OH",
        "Worcester, MA",
        "Tupelo, MS",
        "Lubbock, TX"
    ]
    
    # Get coordinates for each city
    city_coords = {city: get_lat_lon(city) for city in cities}
    
    # Define the graph with distances as weights
    graph = {
        "Gilroy, CA": {"Cheyenne, WY": calculate_distance(*city_coords["Gilroy, CA"], *city_coords["Cheyenne, WY"])},
        "Cheyenne, WY": {"Fargo, ND": calculate_distance(*city_coords["Cheyenne, WY"], *city_coords["Fargo, ND"]),
                         "Lubbock, TX": calculate_distance(*city_coords["Cheyenne, WY"], *city_coords["Lubbock, TX"])},
        "Fargo, ND": {"Zanesville, OH": calculate_distance(*city_coords["Fargo, ND"], *city_coords["Zanesville, OH"])},
        "Tupelo, MS": {"Lubbock, TX": calculate_distance(*city_coords["Tupelo, MS"], *city_coords["Lubbock, TX"]),
                       "Zanesville, OH": calculate_distance(*city_coords["Tupelo, MS"], *city_coords["Zanesville, OH"])},
        "Zanesville, OH": {"Worcester, MA": calculate_distance(*city_coords["Zanesville, OH"], *city_coords["Worcester, MA"])},
        "Worcester, MA": {"Tupelo, MS": calculate_distance(*city_coords["Worcester, MA"], *city_coords["Tupelo, MS"])},
        "Lubbock, TX": {"Gilroy, CA": calculate_distance(*city_coords["Lubbock, TX"], *city_coords["Gilroy, CA"]),
                        "Fargo, ND": calculate_distance(*city_coords["Lubbock, TX"], *city_coords["Fargo, ND"]),
                        "Zanesville, OH": calculate_distance(*city_coords["Lubbock, TX"], *city_coords["Zanesville, OH"])}
    }
    
    # Solve the shortest path problems
    print("Shortest route from Gilroy to Lubbock:")
    print(dijkstra(graph, "Gilroy, CA", "Lubbock, TX"))

    print("\nShortest route from Gilroy to Zanesville:")
    print(dijkstra(graph, "Gilroy, CA", "Zanesville, OH"))

    print("\nShortest route from Tupelo to Fargo:")
    print(dijkstra(graph, "Tupelo, MS", "Fargo, ND"))

    print("\nShortest route from Worcester to Gilroy:")
    print(dijkstra(graph, "Worcester, MA", "Gilroy, CA"))

if __name__ == "__main__":
    main()
