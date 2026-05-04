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
models = snapshot["models"]



# STEP 2 — BUILD GRAPH

graph = nx.DiGraph()


for source, targets in dependencies.items():

    for target in targets:

        graph.add_edge(source, target)



# STEP 3 — FIND WORKFLOW PATHS

def find_workflow(keyword):

    keyword = keyword.lower()


    matching_apps = []


    # MATCH APPS

    for app in graph.nodes:

        if keyword in app.lower():

            matching_apps.append(app)


    # MATCH MODELS

    for app, model_list in models.items():

        for model in model_list:

            if keyword in model.lower():

                matching_apps.append(app)


    matching_apps = list(set(matching_apps))


    # BUILD WORKFLOW CHAINS

    workflows = []


    for app in matching_apps:

        descendants = nx.descendants(
            graph,
            app
        )


        if descendants:

            workflow = [app]

            workflow.extend(
                sorted(descendants)
            )

            workflows.append(workflow)


    return workflows


# STEP 4 — INTERACTIVE LOOP

print("\nWORKFLOW MAPPER\n")


while True:

    keyword = input(
        "\nWorkflow keyword (or exit): "
    )


    if keyword.lower() == "exit":

        break


    results = find_workflow(keyword)


    if results:

        print("\nPOSSIBLE WORKFLOWS:\n")


        for workflow in results:

            print(
                " → ".join(workflow)
            )

    else:

        print("\nNo workflow found")