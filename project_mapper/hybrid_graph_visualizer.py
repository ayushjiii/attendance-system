from pathlib import Path
import json
from pyvis.network import Network



# FILES


INPUT_FILE = Path(
    "snapshots/hybrid/filtered_call_graph.json"
)

OUTPUT_FILE = (
    "outputs/html/hybrid_graph.html"
)



# LOAD GRAPH


with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    call_graph = json.load(f)



# CREATE NETWORK

net = Network(
    height="900px",
    width="100%",
    directed=True,
    bgcolor="#111111",
    font_color="white"
)


net.toggle_physics(False)


# TRACKERS

added_nodes = set()
added_edges = set()



# BUILD GRAPH


for caller, callees in call_graph.items():

    if caller not in added_nodes:

        net.add_node(
            caller,
            label=caller,
            size=20
        )

        added_nodes.add(caller)


    for callee in callees:


        if callee not in added_nodes:

            net.add_node(
                callee,
                label=callee,
                size=10
            )

            added_nodes.add(callee)


        edge = (caller, callee)


        if edge not in added_edges:

            net.add_edge(
                caller,
                callee
            )

            added_edges.add(edge)



#SAVE

net.write_html(
    OUTPUT_FILE,
    notebook=False
)


print("\nHYBRID GRAPH CREATED\n")