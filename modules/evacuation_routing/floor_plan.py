import networkx as nx
import matplotlib.pyplot as plt
import os

def create_floor_plan_graph():
    """
    Creates and returns a NetworkX graph representing the updated mock floor plan with room numbers.
    """
    G = nx.Graph()
    
    # Add nodes with specific identifiers
    nodes = ["101", "102", "103", "Corridor-A", "Corridor-B", "Lobby", "Exit-1", "Exit-2"]
    G.add_nodes_from(nodes)
    
    # Add edges representing physical connections (doorways/hallways)
    edges = [
        ("101", "Corridor-A"),
        ("102", "Corridor-A"),
        ("103", "Corridor-B"),
        ("Corridor-A", "Lobby"),
        ("Corridor-B", "Lobby"),
        ("Lobby", "Exit-1"),
        ("Corridor-B", "Exit-2"),
        ("102", "Corridor-B")  # Room 102 has access to both corridors
    ]
    # Add default distance of 1 to all edges to make the graph weighted
    weighted_edges = [(u, v, {"distance": 1}) for u, v in edges]
    G.add_edges_from(weighted_edges)
    
    return G

def find_escape_route(graph, fire_origin_room, blocked_rooms=None):
    """
    Takes a fire_origin_room and returns the ONE most feasible escape route from that origin.
    It avoids returning to the fire origin and avoids any adjacent blocked rooms.
    """
    if blocked_rooms is None:
        blocked_rooms = []
        
    exits = ["Exit-1", "Exit-2"]
    safe_graph = graph.copy()
    
    # We remove blocked rooms so they cannot be traversed
    for node in blocked_rooms:
        if node in safe_graph and node != fire_origin_room and node not in exits:
            safe_graph.remove_node(node)
            
    best_path = None
    shortest_len = float('inf')
    
    # Find the shortest safe path to any of the available exits
    for exit_node in exits:
        try:
            path = nx.dijkstra_path(safe_graph, source=fire_origin_room, target=exit_node, weight="distance")
            if len(path) < shortest_len:
                shortest_len = len(path)
                best_path = path
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            continue
            
    if best_path is None:
        print(f"No safe route available from {fire_origin_room} — all paths blocked.")
            
    return best_path

def plot_floor_plan(graph, fire_origin_room, path, filename="evacuation_route.png"):
    """
    Plots the graph using matplotlib. 
    Highlights the fire origin room in red, the recommended escape path in green, 
    and labels every room with its number.
    """
    plt.figure(figsize=(10, 8))
    
    # Define a logical layout for the floor plan
    pos = {
        "101": (0.2, 0.8),
        "102": (0.5, 0.8),
        "103": (0.8, 0.8),
        "Corridor-A": (0.35, 0.5),
        "Corridor-B": (0.65, 0.5),
        "Lobby": (0.5, 0.2),
        "Exit-1": (0.5, 0.0),
        "Exit-2": (0.9, 0.5)
    }
    
    # Draw base nodes and edges
    nx.draw_networkx_nodes(graph, pos, node_color='lightgray', node_size=2500, edgecolors='black')
    nx.draw_networkx_edges(graph, pos, edge_color='gray', width=2)
    nx.draw_networkx_labels(graph, pos, font_size=10, font_weight='bold')
    
    # Highlight the recommended escape path
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color='lightgreen', node_size=2500, edgecolors='green', linewidths=2)
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='green', width=4)
    else:
        # Add annotation if no route is found
        if fire_origin_room in pos:
            plt.text(pos[fire_origin_room][0], pos[fire_origin_room][1] - 0.15, "No safe route available", 
                     color='red', fontsize=12, fontweight='bold', ha='center', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
        
    # Highlight the fire origin room in RED (overrides path coloring for this specific node)
    if fire_origin_room in graph:
        nx.draw_networkx_nodes(graph, pos, nodelist=[fire_origin_room], node_color='salmon', node_size=2500, edgecolors='red', linewidths=3)

    plt.title(f"Evacuation Route from Fire Origin ({fire_origin_room})", fontsize=16)
    plt.axis('off')
    
    # Save the plot
    save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    return save_path

if __name__ == "__main__":
    print("Setting up updated Evacuation Routing Module...")
    G = create_floor_plan_graph()
    
    fire_room = "102"
    
    # Test 1: No blocks
    best_escape_1 = find_escape_route(G, fire_origin_room=fire_room, blocked_rooms=[])
    print(f"\nTest 1 (No blocks) - Fire detected in: {fire_room}")
    print(f"Recommended Escape Route: {best_escape_1}")
    plot_path_1 = plot_floor_plan(G, fire_origin_room=fire_room, path=best_escape_1, filename="test_fire_102_route_noblocks.png")
    print(f"Evacuation plot saved to: {plot_path_1}")
    
    # Test 2: Corridor-B blocked
    best_escape_2 = find_escape_route(G, fire_origin_room=fire_room, blocked_rooms=["Corridor-B"])
    print(f"\nTest 2 (Corridor-B blocked) - Fire detected in: {fire_room}")
    print(f"Recommended Escape Route: {best_escape_2}")
    plot_path_2 = plot_floor_plan(G, fire_origin_room=fire_room, path=best_escape_2, filename="test_fire_102_route_block_B.png")
    print(f"Evacuation plot saved to: {plot_path_2}")
    
    # Test 3: Both Corridors blocked
    best_escape_3 = find_escape_route(G, fire_origin_room=fire_room, blocked_rooms=["Corridor-A", "Corridor-B"])
    print(f"\nTest 3 (Both Corridors blocked) - Fire detected in: {fire_room}")
    print(f"Recommended Escape Route: {best_escape_3}")
    plot_path_3 = plot_floor_plan(G, fire_origin_room=fire_room, path=best_escape_3, filename="test_fire_102_route_block_both.png")
    print(f"Evacuation plot saved to: {plot_path_3}")
