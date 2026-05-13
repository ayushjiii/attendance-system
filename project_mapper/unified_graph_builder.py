import ast
import json
import os
from pathlib import Path


# config

PROJECT_ROOT = Path("../").resolve()

OUTPUT_FILE = Path(
    "snapshots/unified/unified_graph.json"
)

IGNORED_FOLDERS = {

    "venv",
    "__pycache__",
    ".git",
    "snapshots",
    "node_modules",
    "migrations"
}


# graph storage

nodes = {}

edges = []

edge_set = set()


# ignored noisy calls

IGNORED_CALLS = {

    "print",
    "len",
    "int",
    "str",
    "float",
    "dict",
    "list",
    "set",
    "tuple",
    "min",
    "max",
    "sum",
    "range",
    "input",
    "type",
    "isinstance",
    "sorted",
    "round",
    "redirect",
    "render"
}


# ignored noisy attrs

IGNORED_ATTRS = {

    "filter",
    "get",
    "all",
    "first",
    "last",
    "exists",
    "count",
    "split",
    "strip",
    "append",
    "extend",
    "lower",
    "upper",
    "save",
    "delete",
    "order_by",
    "select_related",
    "prefetch_related",
    "objects"
}


# known django model names

KNOWN_MODEL_HINTS = {

    "AttendanceRecord",
    "Employee",
    "LeaveRequest",
    "Holiday"
}


# add node

def add_node(node_id, node_type, file_path):

    if not node_id:

        return

    if node_id not in nodes:

        nodes[node_id] = {

            "id": node_id,

            "type": node_type,

            "file": str(file_path)
        }


# add edge

def add_edge(source, target, relation):

    if not source or not target:

        return

    edge_key = (

        source,
        target,
        relation
    )

    if edge_key in edge_set:

        return

    edge_set.add(edge_key)

    edges.append({

        "source": source,

        "target": target,

        "relation": relation
    })


# graph visitor

class GraphVisitor(ast.NodeVisitor):

    def __init__(self, file_path):

        self.file_path = file_path

        self.current_function = None

        self.current_class = None

        self.module_name = file_path.stem

        self.variable_models = {}


    # imports

    def visit_Import(self, node):

        for alias in node.names:

            add_edge(

                str(self.file_path),

                alias.name,

                "imports"
            )

        self.generic_visit(node)


    # from imports

    def visit_ImportFrom(self, node):

        if node.module:

            add_edge(

                str(self.file_path),

                node.module,

                "imports"
            )

        self.generic_visit(node)


    # classes

    def visit_ClassDef(self, node):

        self.current_class = node.name

        class_name = node.name

        node_type = "class"

        for base in node.bases:

            if isinstance(base, ast.Name):

                if base.id == "Model":

                    node_type = "model"

                elif "Form" in base.id:

                    node_type = "form"

                elif "Admin" in base.id:

                    node_type = "admin"

                elif "View" in base.id:

                    node_type = "view_class"

            elif isinstance(base, ast.Attribute):

                if base.attr == "Model":

                    node_type = "model"

        if node_type == "model":

            node_id = f"model.{class_name}"

        else:

            node_id = f"{node_type}.{class_name}"

        add_node(

            node_id,
            node_type,
            self.file_path
        )

        self.generic_visit(node)


    # functions

    def visit_FunctionDef(self, node):

        self.current_function = node.name

        node_type = "function"

        if node.name.endswith("_view"):

            node_type = "view"

        node_id = (

            f"{self.module_name}."
            f"{node.name}"
        )

        add_node(

            node_id,
            node_type,
            self.file_path
        )

        self.generic_visit(node)


    # async functions

    def visit_AsyncFunctionDef(self, node):

        self.visit_FunctionDef(node)


    # assignment tracking

    def visit_Assign(self, node):

        if isinstance(node.value, ast.Call):

            call = node.value

            if isinstance(call.func, ast.Attribute):

                value = call.func.value

                if isinstance(value, ast.Attribute):

                    if isinstance(value.value, ast.Name):

                        model_name = value.value.id

                        if model_name in KNOWN_MODEL_HINTS:

                            for target in node.targets:

                                if isinstance(target, ast.Name):

                                    self.variable_models[

                                        target.id

                                    ] = model_name

        self.generic_visit(node)


    # calls

    def visit_Call(self, node):

        if not self.current_function:

            self.generic_visit(node)

            return

        source_id = (

            f"{self.module_name}."
            f"{self.current_function}"
        )

        # direct calls

        if isinstance(node.func, ast.Name):

            called = node.func.id

            if called not in IGNORED_CALLS:

                add_edge(

                    source_id,
                    called,
                    "calls"
                )

        # attribute calls

        elif isinstance(node.func, ast.Attribute):

            attr = node.func.attr

            value = node.func.value

            # template rendering

            if attr == "render":

                for arg in node.args:

                    if isinstance(arg, ast.Constant):

                        if isinstance(arg.value, str):

                            add_edge(

                                source_id,
                                arg.value,
                                "renders"
                            )

            # detect direct model usage

            if isinstance(value, ast.Name):

                object_name = value.id

                # variable tracked model

                if object_name in self.variable_models:

                    model_name = self.variable_models[object_name]

                    add_edge(

                        source_id,
                        f"model.{model_name}",
                        "uses_model"
                    )

                # direct model access

                elif object_name in KNOWN_MODEL_HINTS:

                    add_edge(

                        source_id,
                        f"model.{object_name}",
                        "uses_model"
                    )

            # detect AttendanceRecord.objects.filter()

            elif isinstance(value, ast.Attribute):

                if isinstance(value.value, ast.Name):

                    model_name = value.value.id

                    if model_name in KNOWN_MODEL_HINTS:

                        add_edge(

                            source_id,
                            f"model.{model_name}",
                            "uses_model"
                        )

            # normal call edge

            if attr not in IGNORED_ATTRS:

                add_edge(

                    source_id,
                    attr,
                    "calls"
                )

        self.generic_visit(node)


# extract django urls

def extract_urls(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            source = f.read()

        tree = ast.parse(source)

    except:

        return

    for node in ast.walk(tree):

        if not isinstance(node, ast.Call):

            continue

        if not isinstance(node.func, ast.Name):

            continue

        if node.func.id != "path":

            continue

        if len(node.args) < 2:

            continue

        route = None

        target = None

        if isinstance(

            node.args[0],
            ast.Constant
        ):

            route = node.args[0].value

        second = node.args[1]

        if isinstance(second, ast.Attribute):

            target = (

                f"views."
                f"{second.attr}"
            )

        elif isinstance(second, ast.Name):

            target = (

                f"views."
                f"{second.id}"
            )

        if route and target:

            url_node = f"url:{route}"

            add_node(

                url_node,
                "url",
                file_path
            )

            add_edge(

                url_node,
                target,
                "routes_to"
            )


# collect files

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


# process files

for file_path in python_files:

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            source = f.read()

        tree = ast.parse(source)

        visitor = GraphVisitor(file_path)

        visitor.visit(tree)

        if file_path.name == "urls.py":

            extract_urls(file_path)

    except Exception as e:

        print(f"\nERROR: {file_path}")

        print(e)


# save graph

OUTPUT_FILE.parent.mkdir(

    parents=True,
    exist_ok=True
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(

        {
            "nodes": nodes,
            "edges": edges
        },

        f,
        indent=4
    )


print("\nUNIFIED GRAPH BUILT\n")

print("Nodes:", len(nodes))

print("Edges:", len(edges))