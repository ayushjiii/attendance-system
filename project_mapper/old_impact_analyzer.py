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



# STEP 3 — IMPACT ANALYSIS


def analyze_impact(node_name):

    try:

        affected = nx.descendants(
            graph,
            node_name
        )

        return affected

    except nx.NetworkXError:

        return None


# STEP 4 — INTERACTIVE LOOP


print("\nIMPACT ANALYZER\n")


while True:

    node = input(
        "\nAnalyze node (or exit): "
    )


    if node.lower() == "exit":

        break


    result = analyze_impact(node)


    if result:

        print("\nPOTENTIALLY AFFECTED:\n")

        for item in sorted(result):

            print(f"- {item}")

    elif result == set():

        print("\nNo downstream impact found")

    else:

        print("\nNode not found")