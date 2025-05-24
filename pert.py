import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Define tasks with optimistic, most likely, pessimistic times and dependencies
tasks = {
    'A': {'optimistic': 2, 'most_likely': 4, 'pessimistic': 6, 'dependencies': []},
    'B': {'optimistic': 1, 'most_likely': 2, 'pessimistic': 3, 'dependencies': ['A']},
    'C': {'optimistic': 1, 'most_likely': 3, 'pessimistic': 5, 'dependencies': ['A']},
    'D': {'optimistic': 2, 'most_likely': 2, 'pessimistic': 4, 'dependencies': ['B']},
    'E': {'optimistic': 3, 'most_likely': 5, 'pessimistic': 7, 'dependencies': ['C']},
    'F': {'optimistic': 1, 'most_likely': 4, 'pessimistic': 6, 'dependencies': ['D', 'E']}
}

# Calculate expected duration and variance
for task in tasks:
    o = tasks[task]['optimistic']
    m = tasks[task]['most_likely']
    p = tasks[task]['pessimistic']
    tasks[task]['duration'] = (o + 4 * m + p) / 6
    tasks[task]['variance'] = ((p - o) / 6) ** 2

# Create graph
G = nx.DiGraph()
for task, info in tasks.items():
    G.add_node(task, duration=info['duration'], variance=info['variance'])
    for dep in info['dependencies']:
        G.add_edge(dep, task)

# Topological sort
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

# Critical path = tasks where EST == LST
critical_path = [task for task in G.nodes if abs(earliest_start[task] - latest_start[task]) < 1e-5]

# Project standard deviation from variances along critical path
project_variance = sum(G.nodes[task]['variance'] for task in critical_path)
project_std_dev = np.sqrt(project_variance)

# Output
print("Earliest start times:", earliest_start)
print("Earliest finish times:", earliest_finish)
print("Latest start times:", latest_start)
print("Latest finish times:", latest_finish)
print("Critical path:", critical_path)
print("Project duration (expected):", project_duration)
print("Project standard deviation:", project_std_dev)

# Draw graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{u}→{v}" for u, v in G.edges()})
plt.title("Task Dependency Graph")
plt.show()
