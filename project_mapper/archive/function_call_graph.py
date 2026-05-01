from pathlib import Path
import json
from pyvis.network import Network



# FILE PATHS


CALL_GRAPH_FILE = Path(
    "snapshots/call_graph.json"
)

OUTPUT_FILE = (
    "function_call_graph.html"
)



# LOAD CALL GRAPH


with open(
    CALL_GRAPH_FILE,
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



# PERFORMANCE SETTINGS


# Disable physics for faster rendering
net.toggle_physics(False)

# Optional layout optimization
net.barnes_hut()



# FILTER SETTINGS


# Only include functions with at least
# this many outgoing relationships
MIN_CONNECTIONS = 2



# TRACK DUPLICATES


added_nodes = set()
added_edges = set()



# BUILD GRAPH


for caller, callees in call_graph.items():

    
    # REMOVE DUPLICATES
    

    unique_callees = set(callees)


    
    # FILTER SMALL FUNCTIONS
    

    if len(unique_callees) < MIN_CONNECTIONS:

        continue


    
    # ADD CALLER NODE
    

    if caller not in added_nodes:

        net.add_node(
            caller,
            label=caller,
            title=(
                f"Function: {caller}\n"
                f"Calls: {len(unique_callees)}"
            ),
            shape="dot",
            size=20
        )

        added_nodes.add(caller)


    
    # PROCESS CALLEES
    

    for callee in unique_callees:


        
        # SKIP SELF CALLS
        

        if caller == callee:

            continue


        
        # ADD CALLEE NODE
        

        if callee not in added_nodes:

            net.add_node(
                callee,
                label=callee,
                title=f"Function: {callee}",
                shape="dot",
                size=10
            )

            added_nodes.add(callee)


        
        # ADD EDGE
        

        edge = (caller, callee)


        if edge not in added_edges:

            net.add_edge(
                caller,
                callee
            )

            added_edges.add(edge)



# SAVE HTML


net.write_html(
    OUTPUT_FILE,
    notebook=False
)



# STATS


print("\nFUNCTION CALL GRAPH CREATED\n")

print(f"Nodes: {len(added_nodes)}")
print(f"Edges: {len(added_edges)}")

print(f"\nSaved as: {OUTPUT_FILE}\n")