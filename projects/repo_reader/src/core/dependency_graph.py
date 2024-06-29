from collections import deque
import subprocess
import json
import re

def generate_dependency_graph(project_path):
    result = subprocess.run(['pydeps', '--noshow', '--show-dot', project_path], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error running pydeps:", result.stderr)
        return None
    return parse_dot_output(result.stdout)

def parse_dot_output(dot_output):
    nodes = set()
    edges = []
    for line in dot_output.splitlines():
        if '->' in line:
            src, dst = re.findall(r'"([^"]+)"', line)
            edges.append({'src': src, 'dst': dst})
            nodes.add(src)
            nodes.add(dst)
    return {'nodes': list(nodes), 'edges': edges}

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
project_path = "/Users/varunpasupuleti/Documents/Axos/Axos/projects/repo_reader/app.py"
dependency_graph = generate_dependency_graph(project_path)

if dependency_graph:
    # Get the sorted order of dependencies
    dependency_order = get_dependency_order(dependency_graph)

    # Print the dependency order
    print("Dependency Order:", dependency_order)
    for file_path in dependency_order:
        print(file_path)

    # Refactor files based on the dependency order
    # for file_path in dependency_order:
    #     refactor_file_with_context(file_path)
