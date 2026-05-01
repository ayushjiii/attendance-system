from pathlib import Path
import json



# FILES


INPUT_FILE = Path(
    "snapshots/raw/detailed_call_graph.json"
)

OUTPUT_FILE = Path(
    "snapshots/hybrid/filtered_call_graph.json"
)



# SETTINGS

MIN_CONNECTIONS = 2


# LOAD GRAPH


with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    call_graph = json.load(f)


# FILTER GRAPH

hybrid_graph = {}


for caller, callees in call_graph.items():

    unique_callees = list(
        set(callees)
    )


    if len(unique_callees) < MIN_CONNECTIONS:

        continue


    hybrid_graph[
        caller
    ] = sorted(unique_callees)



# SAVE


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        hybrid_graph,
        f,
        indent=4
    )


print("\nHYBRID GRAPH CREATED\n")