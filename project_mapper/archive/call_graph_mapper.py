from pathlib import Path
import ast
import json

#project root
PROJECT_ROOT = Path("../")

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


python_files = list(
    PROJECT_ROOT.rglob("*.py")
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