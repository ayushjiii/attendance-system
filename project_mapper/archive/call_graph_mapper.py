from pathlib import Path
import ast
import json
import os

# ignored folders

PROJECT_ROOT = Path(
    "../"
).resolve()


IGNORED_FOLDERS = {

    "venv",

    "__pycache__",

    ".git",

    "snapshots",

    "outputs",

    "node_modules"
}

# load function map
FUNCTION_MAP_FILE = Path(
    "snapshots/raw/detailed_function_map.json"
)


with open(
    FUNCTION_MAP_FILE,
    "r",
    encoding="utf-8"
) as f:

    function_map = json.load(f)


#build project function set

project_functions = set()


for file_data in function_map.values():

    for func in file_data["functions"]:

        project_functions.add(func)


    for methods in file_data["classes"].values():

        for method in methods:

            project_functions.add(method)


#storage
call_graph = {}



#visitor

class CallGraphVisitor(ast.NodeVisitor):


    def __init__(self):

        self.current_function = None


    def visit_FunctionDef(self, node):

        previous_function = (
            self.current_function
        )


        self.current_function = node.name


        if self.current_function not in call_graph:

            call_graph[
                self.current_function
            ] = []


        self.generic_visit(node)


        self.current_function = (
            previous_function
        )


    def visit_Call(self, node):


        if not self.current_function:

            return


        called_function = None


        if isinstance(node.func, ast.Name):

            called_function = (
                node.func.id
            )


        elif isinstance(
            node.func,
            ast.Attribute
        ):

            called_function = (
                node.func.attr
            )


        if (
            called_function
            and called_function in project_functions
        ):

            call_graph[
                self.current_function
            ].append(
                called_function
            )


        self.generic_visit(node)



# PROCESS FILES

python_files = []


for root, dirs, files in os.walk(PROJECT_ROOT):


    dirs[:] = [

        d for d in dirs

        if d not in IGNORED_FOLDERS
    ]


    for file in files:


        if file.endswith(".py"):


            python_files.append(

                Path(root) / file
            )

for file_path in python_files:

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            source_code = f.read()


        tree = ast.parse(source_code)


        visitor = CallGraphVisitor()

        visitor.visit(tree)


    except Exception:

        continue



# SAVE


OUTPUT_FILE = Path(
    "snapshots/raw/detailed_call_graph.json"
)


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        call_graph,
        f,
        indent=4
    )


print("\nDETAILED CALL GRAPH CREATED\n")