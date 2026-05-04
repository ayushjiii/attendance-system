from pathlib import Path
import json
from collections import defaultdict


# FILES

CALL_GRAPH_FILE = Path(
    "snapshots/raw/detailed_call_graph.json"
)

# LOAD GRAPH

with open(
    CALL_GRAPH_FILE,
    "r",
    encoding="utf-8"
) as f:

    call_graph = json.load(f)



# BUILD REVERSE GRAPH


reverse_graph = defaultdict(list)


for caller, callees in call_graph.items():

    for callee in callees:

        reverse_graph[callee].append(caller)


# IMPACT TRACING

def trace_impact(


    node,

    visited=None,

    depth=0,

    max_depth=4
):


    # INIT VISITED

    if visited is None:

        visited = set()



    # DEPTH LIMIT

    if depth > max_depth:

        return



    # LOOP PREVENTION


    if node in visited:

        return


    visited.add(node)

    indent = "    " * depth

    print(f"{indent}- {node}")


    # WHO DEPENDS ON THIS?
    impacted_nodes = reverse_graph.get(
        node,
        []
    )


    # RECURSIVE REVERSE DFS


    for impacted in impacted_nodes:

        trace_impact(

            impacted,

            visited,

            depth + 1,

            max_depth
        )



# MENU


print("\nIMPACT ANALYZER\n")


while True:


    target = input(

        "\nEnter function/model "
        "(or 'exit'): "

    )


    if target.lower() == "exit":

        break


    print("\nIMPACT CHAIN:\n")


    trace_impact(target)