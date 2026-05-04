from pathlib import Path
import json
from collections import defaultdict


# FILES

MODEL_USAGE_FILE = Path(
    "snapshots/raw/model_usage.json"
)

CALL_GRAPH_FILE = Path(
    "snapshots/raw/detailed_call_graph.json"
)

SNAPSHOT_FILE = Path(
    "snapshots/snapshot.json"
)


# LOAD DATA

with open(
    MODEL_USAGE_FILE,
    "r",
    encoding="utf-8"
) as f:

    model_usage = json.load(f)

with open(
    CALL_GRAPH_FILE,
    "r",
    encoding="utf-8"
) as f:

    call_graph = json.load(f)


with open(
    SNAPSHOT_FILE,
    "r",
    encoding="utf-8"
) as f:

    snapshot = json.load(f)


dependencies = snapshot["dependencies"]
models = snapshot["models"]


# BUILD REVERSE GRAPH

reverse_graph = defaultdict(list)


for caller, callees in call_graph.items():

    for callee in callees:

        reverse_graph[callee].append(caller)


# REVERSE MODEL USAGE

reverse_model_usage = defaultdict(list)


for function, used_models in model_usage.items():

    for model in used_models:

        reverse_model_usage[model].append(
            function
        )



# FUNCTIONS USING MODEL


def get_model_functions(model_name):


    return reverse_model_usage.get(
        model_name,
        []
    )

# WORKFLOW TRACE


def get_workflow(


    node,

    visited=None,

    depth=0,

    max_depth=3
):


    if visited is None:

        visited = set()


    if depth > max_depth:

        return []


    if node in visited:

        return []


    visited.add(node)


    workflow = [node]


    children = call_graph.get(
        node,
        []
    )


    for child in children:

        workflow.extend(

            get_workflow(

                child,

                visited,

                depth + 1,

                max_depth
            )
        )


    return workflow



# IMPACT TRACE


def get_impact(


    node,

    visited=None,

    depth=0,

    max_depth=3
):


    if visited is None:

        visited = set()


    if depth > max_depth:

        return []


    if node in visited:

        return []


    visited.add(node)


    impact = [node]


    parents = reverse_graph.get(
        node,
        []
    )


    for parent in parents:

        impact.extend(

            get_impact(

                parent,

                visited,

                depth + 1,

                max_depth
            )
        )


    return impact


    # MODEL FUNCTIONS


    model_functions = get_model_functions(
        node
    )


    print("\nFUNCTIONS USING MODEL:\n")


    if model_functions:

        for function in model_functions:

            print(f"- {function}")

    else:

        print("- None found")

# RELATED APPS


def find_related_apps(node):


    related = []


    for app, app_models in models.items():

        if node in app_models:

            related.append(app)


    return related



# APP DEPENDENCIES


def get_dependencies(apps):


    results = {}


    for app in apps:

        results[app] = dependencies.get(
            app,
            []
        )


    return results



# CONTEXT RETRIEVAL


def retrieve_context(node):


    print("\n=================================")
    print("ARCHITECTURE CONTEXT")
    print("=================================")


    
    # WORKFLOW
    

    workflow = get_workflow(node)


    print("\nWORKFLOW TRACE:\n")


    for item in workflow:

        print(f"- {item}")


    
    # IMPACT
    

    impact = get_impact(node)


    print("\nIMPACT CHAIN:\n")


    for item in impact:

        print(f"- {item}")


    
    # RELATED APPS
    

    related_apps = find_related_apps(node)


    print("\nRELATED APPS:\n")


    if related_apps:

        for app in related_apps:

            print(f"- {app}")

    else:

        print("- None found")


    
    # DEPENDENCIES
    

    dependency_info = get_dependencies(
        related_apps
    )


    print("\nAPP DEPENDENCIES:\n")


    for app, deps in dependency_info.items():

        print(f"{app} -> {deps}")



# MENU


print("\nCONTEXT RETRIEVER\n")


while True:


    node = input(

        "\nEnter function/model "
        "(or 'exit'): "

    )


    if node.lower() == "exit":

        break


    retrieve_context(node)