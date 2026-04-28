from pathlib import Path
import ast
from collections import defaultdict
import networkx as nx
from pyvis.network import Network


PROJECT_PATH = Path(r"E:\WORK\python\ATTENDENCE")

IGNORE_FOLDERS = {
    "__pycache__",
    ".git",
    "venv",
    "env",
    "node_modules",
    "migrations"
}

python_files = []


# STEP 1 — Collect project apps

PROJECT_APPS = set()

for item in PROJECT_PATH.iterdir():

    if item.is_dir():

        if item.name not in IGNORE_FOLDERS:

            PROJECT_APPS.add(item.name)


# STEP 2 — Collect python files

for file in PROJECT_PATH.rglob("*.py"):

    skip = False

    for part in file.parts:

        if part in IGNORE_FOLDERS:
            skip = True
            break

    if not skip:
        python_files.append(file)


# STEP 3 — Store weighted relationships

relationships = defaultdict(int)


# STEP 4 — Extract dependencies

for file in python_files:

    try:

        with open(file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        current_app = file.parts[-2]

        for node in ast.walk(tree):

            if isinstance(node, ast.ImportFrom):

                module = node.module

                if module:

                    module_parts = module.split(".")

                    imported_app = module_parts[0]

                    if len(module_parts) > 1:
                        imported_component = module_parts[1]
                    else:
                        imported_component = "unknown"

                    if imported_app in PROJECT_APPS:

                        if imported_app != current_app:

                            relationships[
                                (
                                    current_app,
                                    f"{imported_app}.{imported_component}"
                                )
                            ] += 1
    except Exception as e:
        print(f"\nERROR in {file}")
        print(e)


print("\nWEIGHTED DEPENDENCIES:\n")

for (source, target), weight in sorted(relationships.items()):

    print(f"{source} ---> {target} ({weight})")


# STEP 5 — Build graph

graph = nx.DiGraph()

for (source, target), weight in relationships.items():

    graph.add_node(source)
    graph.add_node(target)

    graph.add_edge(
        source,
        target,
        weight=weight
    )


# STEP 6 — Create visualization

net = Network(
    height="750px",
    width="100%",
    directed=True
)

net.from_nx(graph)


# STEP 7 — Add weighted edges manually

net.edges = []

for (source, target), weight in relationships.items():

    net.add_edge(
        source,
        target,
        label=str(weight)
    )


output_file = "attendance_graph.html"

net.save_graph(output_file)

print(f"\nGraph saved as: {output_file}")