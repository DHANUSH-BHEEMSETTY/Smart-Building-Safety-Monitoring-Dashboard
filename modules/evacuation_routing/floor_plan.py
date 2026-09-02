import networkx as nx
import matplotlib.pyplot as plt
import os

def create_floor_plan_graph():
    """
    Creates and returns a NetworkX graph representing the building floor plan with zones and rooms.
    """
    G = nx.Graph()
    
    # Add nodes with specific identifiers matching the building layout
    nodes = ["101", "102", "103", "Corridor-1", "Corridor-2", "Lobby", "Exit-1", "Exit-3"]
    G.add_nodes_from(nodes)
    
    # Add physical doorways/hallway connections
    edges = [
        ("101", "Corridor-1"),
        ("102", "Corridor-1"),
        ("102", "Lobby"),
        ("103", "Corridor-2"),
        ("Corridor-1", "Exit-1"),
        ("Corridor-1", "Lobby"),
        ("Corridor-2", "Lobby"),
        ("Lobby", "Exit-3"),
        ("Corridor-2", "Exit-3")
    ]
    # Add weighted distances
    weighted_edges = [(u, v, {"distance": 1}) for u, v in edges]
    G.add_edges_from(weighted_edges)
    
    return G

def find_escape_route(graph, fire_origin_room, blocked_rooms=None):
    """
    Computes the shortest-safe escape route from fire_origin_room avoiding hazard/blocked zones.
    """
    if blocked_rooms is None:
        blocked_rooms = []
        
    exits = ["Exit-3", "Exit-1"]
    safe_graph = graph.copy()
    
    # Remove blocked rooms so they cannot be traversed
    for node in blocked_rooms:
        if node in safe_graph and node != fire_origin_room and node not in exits:
            safe_graph.remove_node(node)
            
    best_path = None
    shortest_len = float('inf')
    
    # Find the shortest safe path to any available exit
    for exit_node in exits:
        try:
            path = nx.dijkstra_path(safe_graph, source=fire_origin_room, target=exit_node, weight="distance")
            if len(path) < shortest_len:
                shortest_len = len(path)
                best_path = path
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            continue
            
    return best_path

def plot_floor_plan(graph, fire_origin_room, path, filename="evacuation_route.png"):
    """
    Generates a high-tech dark theme floor plan diagram matching the command-center UI.
    """
    fig, ax = plt.subplots(figsize=(9, 6), facecolor='#0B0F19')
    ax.set_facecolor('#0B0F19')
    
    # Define a high-tech structured layout for the floor plan nodes
    pos = {
        "101": (0.2, 0.75),
        "102": (0.5, 0.8),
        "103": (0.8, 0.75),
        "Corridor-1": (0.28, 0.45),
        "Corridor-2": (0.72, 0.45),
        "Lobby": (0.5, 0.45),
        "Exit-1": (0.15, 0.15),
        "Exit-3": (0.85, 0.15)
    }
    
    # Draw dark hallway structural connections
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color='#334155', width=3, alpha=0.7)
    
    # Draw base non-affected nodes (dark slate with subtle blue border)
    other_nodes = [n for n in graph.nodes if n != fire_origin_room and (not path or n not in path)]
    nx.draw_networkx_nodes(graph, pos, nodelist=other_nodes, ax=ax,
                           node_color='#1E293B', node_size=1800,
                           edgecolors='#475569', linewidths=2)
    
    # Highlight safe path edges and nodes in vivid emerald green
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, ax=ax,
                               edge_color='#10B981', width=6, alpha=0.9)
        
        path_nodes_no_origin = [n for n in path if n != fire_origin_room]
        nx.draw_networkx_nodes(graph, pos, nodelist=path_nodes_no_origin, ax=ax,
                               node_color='#065F46', node_size=1900,
                               edgecolors='#34D399', linewidths=3)
    
    # Highlight Fire Origin Node in glowing neon crimson
    if fire_origin_room in graph:
        # Outer glow ring
        nx.draw_networkx_nodes(graph, pos, nodelist=[fire_origin_room], ax=ax,
                               node_color='#7F1D1D', node_size=2400,
                               edgecolors='#EF4444', linewidths=3, alpha=0.4)
        # Inner core
        nx.draw_networkx_nodes(graph, pos, nodelist=[fire_origin_room], ax=ax,
                               node_color='#DC2626', node_size=1800,
                               edgecolors='#FCA5A5', linewidths=2.5)
        
    # Draw exit markers
    for exit_n in ["Exit-1", "Exit-3"]:
        if exit_n in graph:
            border_col = '#34D399' if (path and exit_n in path) else '#64748B'
            fill_col = '#047857' if (path and exit_n in path) else '#1E293B'
            nx.draw_networkx_nodes(graph, pos, nodelist=[exit_n], ax=ax,
                                   node_color=fill_col, node_size=2000,
                                   edgecolors=border_col, linewidths=2.5)

    # Node Labels with high-contrast typography
    labels = {n: n for n in graph.nodes}
    nx.draw_networkx_labels(graph, pos, labels=labels, ax=ax,
                            font_size=9, font_weight='bold', font_color='#F8FAFC',
                            font_family='sans-serif')
    
    # Add title and status banner
    status_str = f"HAZARD ORIGIN: ROOM {fire_origin_room} • OBSTRUCTION-FREE REROUTE TO SAFE EXIT" if path else f"HAZARD ORIGIN: {fire_origin_room}"
    ax.set_title(status_str, fontsize=11, fontweight='bold', color='#38BDF8', pad=15)
    
    # Add custom legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Hazard Node (Origin)', markerfacecolor='#DC2626', markersize=10, markeredgecolor='#EF4444'),
        plt.Line2D([0], [0], marker='o', color='w', label='Recommended Safe Path', markerfacecolor='#065F46', markersize=10, markeredgecolor='#34D399'),
        plt.Line2D([0], [0], color='#10B981', lw=3, label='Safe Exit Trajectory'),
        plt.Line2D([0], [0], marker='o', color='w', label='Clear Building Zone', markerfacecolor='#1E293B', markersize=9, markeredgecolor='#475569')
    ]
    ax.legend(handles=legend_elements, loc='upper right', facecolor='#0F172A', edgecolor='#334155',
              fontsize=8, labelcolor='#E2E8F0', framealpha=0.9)
    
    ax.axis('off')
    plt.tight_layout()
    
    save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
    plt.savefig(save_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close(fig)
    return save_path
