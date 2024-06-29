from collections import deque
import subprocess
import re

def generate_dependency_graph(project_path):
    result = subprocess.run(['pydeps', '--no-output', '--noshow','--verbose', '--show-dot', '--show-cycles', project_path], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error running pydeps:", result.stderr)
        return None
    return parse_dot_output(result.stdout)

def parse_dot_output(dot_output):
    nodes = set()
    edges = []
    for line in dot_output.splitlines():
        if '->' in line:
            matches = re.findall(r'(\w+)', line)
            if len(matches) >= 2:
                src, dst = matches[0], matches[1]
                edges.append((src, dst))
                nodes.add(src)
                nodes.add(dst)
    return nodes, edges

def create_adjacency_list(nodes, edges):
    adjacency_list = {node: [] for node in nodes}
    for src, dst in edges:
        adjacency_list[src].append(dst)
    return adjacency_list

def get_dependency_order(adjacency_list):
    in_degree = {node: 0 for node in adjacency_list}
    for src in adjacency_list:
        for dst in adjacency_list[src]:
            in_degree[dst] += 1

    queue = deque([node for node in adjacency_list if in_degree[node] == 0])
    sorted_order = []

    while queue:
        node = queue.popleft()
        sorted_order.append(node)
        for neighbor in adjacency_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_order

# Generate the dependency graph
project_path = "/Users/varunpasupuleti/Documents/Axos/Axos/projects/repo_reader/app.py"
nodes, edges = generate_dependency_graph(project_path)

if nodes and edges:
    # Create the adjacency list
    adjacency_list = create_adjacency_list(nodes, edges)
    
    # Get the sorted order of dependencies
    dependency_order = get_dependency_order(adjacency_list)

    # Print the dependency order
    print("Dependency Order:", dependency_order)
    for file_path in dependency_order:
        print(file_path)

    # Refactor files based on the dependency order
    # for file_path in dependency_order:
    #     refactor_file_with_context(file_path)
