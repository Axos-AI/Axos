import ast
import os
import subprocess
import json

class CodeAnalyzer:
    def __init__(self, code_base_path, entry_point):
        self.code_base_path = code_base_path
        self.entry_point = entry_point # format: "src/main.py"
        self.full_entry_point = os.path.join(self.code_base_path, self.entry_point)
        self.dependencies = {}
        self.generate_dependency_graph()
        self.adjacency_list = self.build_adjacency_list(self.validate_dependencies_and_return_tree())
        self.topological_order = self.topological_sort()
        self.refactor_order = self.topological_order[::-1]  # reverse again and start with util/config files, then move to core logic, and finally to main/entry point

    def analyze(self):
        for root, _, files in os.walk(self.code_base_path):
            for file in files:
                if file.endswith('.py'):
                    with open(os.path.join(root, file), 'r') as f:
                        try:
                            tree = ast.parse(f.read())
                            # Perform analysis on the AST
                            self._analyze_tree(tree)
                        except Exception as e:
                            print(f"Error parsing file {file}: {e}")

    def _analyze_tree(self, tree):
        # Implement analysis logic here
        pass

    def generate_dependency_graph(self):
        try:
            result = subprocess.run(
                ["dep-tree", "tree", self.full_entry_point, "--json"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print("Error running dep-tree:", result.stderr)
                return None
            
            # Parse the JSON output
            dependencies = json.loads(result.stdout)
            self.dependencies = dependencies
        
        except Exception as e:
            print("An error occurred:", str(e))
            return None


    def validate_dependencies_and_return_tree(self):
        if self.dependencies is None:
            raise ValueError("Invalid dependencies: empty or None")
        if self.dependencies.get("error"):
            raise ValueError(f"Error in dependency analysis: {self.dependencies['error']}")
        if self.dependencies.get("circularDependencies"):
            raise ValueError(f"Circular dependencies detected: {self.dependencies['circularDependencies']}")
        if not self.dependencies.get("tree"):
            raise ValueError(f"No dependency tree found: {self.dependencies}")
        return self.dependencies["tree"]


    def build_adjacency_list(self, tree):
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


    def topological_sort(self):
        visited = set()
        stack = []
        
        def dfs(node):
            visited.add(node)
            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    dfs(neighbor)
            stack.append(node)
        
        for node in self.adjacency_list:
            if node not in visited:
                dfs(node)
        
        return stack[::-1] # reverse the stack to get the topological order


    def get_refactor_order(self):
        return self.refactor_order

    def get_adjacency_list(self):
        return self.adjacency_list

