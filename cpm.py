import networkx as nx 
import matplotlib.pyplot as plt

tasks = {
    'A': {'duration': 3, 'dependencies': []},
    'B': {'duration': 2, 'dependencies': ['A']},
    'C': {'duration': 4, 'dependencies': ['A']},
    'D': {'duration': 2, 'dependencies': ['B']},
    'E': {'duration': 3, 'dependencies': ['C']},
    'F': {'duration': 1, 'dependencies': ['D', 'E']}
}

G = nx.DiGraph()

for task, info in tasks.items():
    G.add_node(task, duration = info['duration'])
    for dep in info['dependencies']:
        G.add_edge(dep, task)

order = list(nx.topological_sort(G))

# Forward pass: earliest times
earliest_start = {}
earliest_finish = {}
for task in order:
    start = max([earliest_finish.get(dep, 0) for dep in G.predecessors(task)], default=0)
    earliest_start[task] = start
    earliest_finish[task] = start + G.nodes[task]['duration']

# Backward pass: latest times
project_duration = max(earliest_finish.values())
latest_finish = {task: project_duration for task in G.nodes}
latest_start = {}

for task in reversed(order):
    finish = min([latest_start.get(succ, project_duration) for succ in G.successors(task)], default=project_duration)
    latest_finish[task] = finish
    latest_start[task] = finish - G.nodes[task]['duration']

critical_path = [task for task in order if earliest_start[task] == latest_start[task]]
print("Earliest start times:", earliest_start)
print("Earliest finish times:", earliest_finish)
print("Latest start times:", latest_start)
print("Latest finish times:", latest_finish)
print("Critical path:", critical_path)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels = True, node_size = 3000, node_color = "lightgreen")
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u,v ): f"{u}->{v}"for u,v in G.edges})
plt.title("Task Dependency Graph")
plt.show()
