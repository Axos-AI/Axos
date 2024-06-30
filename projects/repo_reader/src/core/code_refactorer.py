import os
import json


class CodeRefactorer:
    def __init__(self, code_base_path, entry_point, ai, refactor_order, adjacency_list):
        self.code_base_path = code_base_path
        self.entry_point = entry_point
        self.relative_path = os.path.join(self.code_base_path, os.path.dirname(self.entry_point))
        self.ai = ai
        self.refactor_order = refactor_order
        self.adjacency_list = adjacency_list

    def refactor(self):
        refactored_files = {}
        
        for file in self.refactor_order:
            file_path = os.path.join(self.relative_path, file)
            
            if os.path.exists(file_path) and file.endswith('.py'):
                with open(file_path, 'r') as f:
                    code = f.read()
                    dependencies = self.adjacency_list.get(file, [])
                    context = self._gather_context(dependencies, refactored_files)
                    refactored_code, logged_changes = self.ai.refactor(code, context) # Pass context
                    
                # Write the refactored code back to the original file
                with open(file_path, 'w') as f:
                    f.write(refactored_code)
                
                # Create a log file next to the original file
                log_file_path = file_path + '.log'
                with open(log_file_path, 'w') as log_f:
                    log_f.write(logged_changes)
                
                # Store the refactored code in the dictionary
                refactored_files[file] = refactored_code

    def _gather_context(self, dependencies, refactored_files):
        context = {}
        for dep in dependencies:
            if dep in refactored_files:
                context[dep] = refactored_files[dep]
        return json.dumps(context, indent=4)