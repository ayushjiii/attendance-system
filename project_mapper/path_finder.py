from pathlib import Path
import json
import networkx as nx


SNAPSHOT_FILE = Path(
    "snapshots/snapshot.json"
)

# STEP 1 — LOAD SNAPSHOT

with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:

    snapshot = json.load(f)


dependencies = snapshot["dependencies"]
relationships = snapshot["model_relationships"]

# STEP 2 — BUILD GRAPH

graph = nx.DiGraph()

## app dependency

for source, targets in dependencies.items():

    for target in targets:

        graph.add_edge(source, target)

## model relationship

for model, relation_list in relationships.items():

    for relation in relation_list:

        target = relation["target"]

        graph.add_edge(model, target)


# setp 3 - path finder function

def find_path(start, end):

    try:

        path = nx.shortest_path(
            graph,
            source=start,
            target=end
        )

        return path

    except nx.NetworkXNoPath:

        return None

    except nx.NodeNotFound:

        return None

# STEP 4 — INTERACTIVE LOOP


print("\nGRAPH PATH FINDER\n")


while True:

    start = input(
        "\nStart node (or exit): "
    )

    if start.lower() == "exit":

        break


    end = input("End node: ")


    result = find_path(start, end)


    if result:

        print("\nFOUND PATH:\n")

        print(" → ".join(result))

    else:

        print("\nNo path found")