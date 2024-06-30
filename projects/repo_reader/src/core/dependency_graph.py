import subprocess
import json

def generate_dependency_graph(project_path):
    try:
        result = subprocess.run(
            ["dep-tree", "tree", project_path, "--json"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("Error running dep-tree:", result.stderr)
            return None
        
        # Parse the JSON output
        dependencies = json.loads(result.stdout)
        return dependencies
    
    except Exception as e:
        print("An error occurred:", str(e))
        return None


def validate_dependencies_and_return_tree(dependencies):
    if dependencies is None:
        raise ValueError("Invalid dependencies: empty or None")
    if dependencies.get("error"):
        raise ValueError(f"Error in dependency analysis: {dependencies['error']}")
    if dependencies.get("circularDependencies"):
        raise ValueError(f"Circular dependencies detected: {dependencies['circularDependencies']}")
    if not dependencies.get("tree"):
        raise ValueError(f"No dependency tree found: {dependencies}")
    return dependencies["tree"]


def build_adjacency_list(tree):
    adjacency_list = {}
    # recursively parse the tree until value is null
    # when value is null, we have reached the leaf node
    def parse_tree(sub_tree):
        for key in sub_tree:
            if key not in adjacency_list:
                adjacency_list[key] = set()
            if sub_tree[key]:
                for child in sub_tree[key]:
                    adjacency_list[key].add(child)
                    parse_tree(sub_tree[key])
                    
    parse_tree(tree)   
    for key in adjacency_list:
        adjacency_list[key] = list(adjacency_list[key]) 
    return adjacency_list


def topological_sort(adjacency_list):
    visited = set()
    stack = []
    
    def dfs(node):
        visited.add(node)
        for neighbor in adjacency_list[node]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)
    
    for node in adjacency_list:
        if node not in visited:
            dfs(node)
    
    return stack[::-1] # reverse the stack to get the topological order




# Example usage
project_path = "/Users/varunpasupuleti/Documents/Axos/Axos/projects/repo_reader/app.py"
dependencies = generate_dependency_graph(project_path)
tree = validate_dependencies_and_return_tree(dependencies)
adjacency_list = build_adjacency_list(tree)
topological_order = topological_sort(adjacency_list)
refactor_order = topological_order[::-1] # reverse again and start with util/config files, then move to core logic, and finally to main/entry point
