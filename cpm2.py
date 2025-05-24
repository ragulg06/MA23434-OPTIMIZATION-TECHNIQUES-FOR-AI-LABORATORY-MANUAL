import networkx as nx
import matplotlib.pyplot as plt

# Define the activities and durations
edges = [
    (0, 1, 2),
    (1, 2, 8),
    (1, 3, 10),
    (2, 4, 6),
    (3, 4, 3),
    (2, 5, 3),
    (3, 6, 7),
    (5, 7, 2),
    (6, 7, 8),
    (4, 7, 5),
]

# Create a directed graph
G = nx.DiGraph()

# Add edges with duration as weight
for u, v, duration in edges:
    G.add_edge(u, v, duration=duration)

# Topological order
order = list(nx.topological_sort(G))

# Earliest start and finish times
earliest_start = {}
earliest_finish = {}
for node in order:
    est = max([earliest_finish.get(pred, 0) for pred in G.predecessors(node)], default=0)
    earliest_start[node] = est
    earliest_finish[node] = est + max([G.edges[pred, node]['duration'] for pred in G.predecessors(node)], default=0)

# Project duration
project_duration = max(earliest_finish.values())

# Latest start and finish times (init to project duration)
latest_finish = {node: project_duration for node in G.nodes}
latest_start = {node: project_duration for node in G.nodes}

# Reverse order for latest times
for node in reversed(order):
    for succ in G.successors(node):
        lft = latest_start[succ] - G.edges[node, succ]['duration']
        latest_finish[node] = min(latest_finish[node], latest_start[succ])
        latest_start[node] = min(latest_start[node], lft)

# Critical path
critical_path = [node for node in G.nodes if earliest_start[node] == latest_start[node]]

# Print results
print("Earliest Start Times:", earliest_start)
print("Earliest Finish Times:", earliest_finish)
print("Latest Start Times:", latest_start)
print("Latest Finish Times:", latest_finish)
print("Project Duration:", project_duration)
print("Critical Path:", critical_path)

# Draw the graph
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=12)
edge_labels = {(u, v): f"{G[u][v]['duration']}" for u, v in G.edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Activity Network Diagram (CPM)")
plt.show()
