from collections import deque
import subprocess
import json

def generate_dependency_graph(project_path):
    result = subprocess.run(['pydeps', '--noshow', '--no-output', '--output-format=json', project_path], capture_output=True, text=True)
    print(result)
    dependency_graph = json.loads(result.stdout)
    return dependency_graph

def get_dependency_order(dependency_graph):
    nodes = dependency_graph['nodes']
    edges = dependency_graph['edges']
    
    in_degree = {node: 0 for node in nodes}
    graph = {node: [] for node in nodes}
    
    for edge in edges:
        src, dst = edge['src'], edge['dst']
        graph[src].append(dst)
        in_degree[dst] += 1

    queue = deque([node for node in nodes if in_degree[node] == 0])
    sorted_order = []

    while queue:
        node = queue.popleft()
        sorted_order.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_order

# Generate the dependency graph
project_path = "/Users/varunpasupuleti/Documents/Axos/Axos/projects/repo_reader"
dependency_graph = generate_dependency_graph(project_path)

# Get the sorted order of dependencies
dependency_order = get_dependency_order(dependency_graph)

# Print the dependency order
print("Dependency Order:", dependency_order)
for file_path in dependency_order:
    print(file_path)

# Refactor files based on the dependency order
# for file_path in dependency_order:
#     refactor_file_with_context(file_path)
