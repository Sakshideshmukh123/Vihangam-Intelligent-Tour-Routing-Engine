import streamlit as st
import heapq
import folium
from streamlit_folium import folium_static

# ---------------- GRAPH ----------------
graph = {
    'Mumbai': {'Pune': 150, 'Nashik': 165, 'Thane': 25},
    'Thane': {'Mumbai': 25, 'Nashik': 140},
    'Pune': {'Mumbai': 150, 'Nashik': 210, 'Satara': 115, 'Ahmednagar': 120},
    'Nashik': {'Mumbai': 165, 'Thane': 140, 'Pune': 210, 'Dhule': 160},
    'Dhule': {'Nashik': 160, 'Jalgaon': 100},
    'Jalgaon': {'Dhule': 100, 'Buldhana': 150},
    'Buldhana': {'Jalgaon': 150, 'Akola': 100, 'Aurangabad': 180},
    'Akola': {'Buldhana': 100, 'Amravati': 100},
    'Amravati': {'Akola': 100, 'Nagpur': 150},
    'Nagpur': {'Amravati': 150, 'Wardha': 80, 'Chandrapur': 150},
    'Wardha': {'Nagpur': 80, 'Yavatmal': 110},
    'Yavatmal': {'Wardha': 110, 'Nanded': 180},
    'Nanded': {'Yavatmal': 180, 'Latur': 110},
    'Latur': {'Nanded': 110, 'Solapur': 150},
    'Solapur': {'Latur': 150, 'Pune': 250},
    'Satara': {'Pune': 115, 'Kolhapur': 120},
    'Kolhapur': {'Satara': 120},
    'Ahmednagar': {'Pune': 120, 'Aurangabad': 115},
    'Aurangabad': {'Ahmednagar': 115, 'Buldhana': 180},
    'Chandrapur': {'Nagpur': 150}
}

# ---------------- COORDINATES ----------------
coords = {
    'Mumbai': (19.0760, 72.8777),
    'Thane': (19.2183, 72.9781),
    'Pune': (18.5204, 73.8567),
    'Nashik': (19.9975, 73.7898),
    'Dhule': (20.9042, 74.7749),
    'Jalgaon': (21.0077, 75.5626),
    'Buldhana': (20.5293, 76.1840),
    'Akola': (20.7002, 77.0082),
    'Amravati': (20.9374, 77.7796),
    'Nagpur': (21.1458, 79.0882),
    'Wardha': (20.7453, 78.6022),
    'Yavatmal': (20.3899, 78.1307),
    'Nanded': (19.1383, 77.3210),
    'Latur': (18.4088, 76.5604),
    'Solapur': (17.6599, 75.9064),
    'Satara': (17.6805, 74.0183),
    'Kolhapur': (16.7050, 74.2433),
    'Ahmednagar': (19.0948, 74.7480),
    'Aurangabad': (19.8762, 75.3433),
    'Chandrapur': (19.9615, 79.2961)
}

# ---------------- DIJKSTRA ----------------
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}

    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous

# ---------------- PATH ----------------
def get_path(previous, start, end):
    path = []
    while end is not None:
        path.append(end)
        end = previous[end]
    return path[::-1]

# ---------------- UI ----------------
st.title("🌍 Vihangam Smart Route Planner")

start_city = st.selectbox("Select Starting City", list(graph.keys()))
end_city = st.selectbox("Select Destination City", list(graph.keys()))

if st.button("Find Best Route"):

    distances, previous = dijkstra(graph, start_city)
    path = get_path(previous, start_city, end_city)

    # Center map dynamically
    center_lat = sum(coords[c][0] for c in path) / len(path)
    center_lon = sum(coords[c][1] for c in path) / len(path)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

    # Mark only path cities (clean UI)
    for city in path:
        color = "green" if city == start_city else "red" if city == end_city else "blue"
        folium.Marker(
            coords[city],
            popup=city,
            icon=folium.Icon(color=color)
        ).add_to(m)

    # Draw path
    folium.PolyLine(
        [coords[city] for city in path],
        color="red",
        weight=6
    ).add_to(m)

    folium_static(m)

    # Output
    st.subheader("📍 Shortest Path")
    st.success(" → ".join(path))

    st.subheader("📊 Total Distance")
    st.info(f"{distances[end_city]} km")