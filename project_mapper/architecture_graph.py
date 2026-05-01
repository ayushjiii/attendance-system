from pathlib import Path
import json

import networkx as nx
from pyvis.network import Network


SNAPSHOT_FILE = Path("snapshots/snapshot.json")


# STEP 1 — Load snapshot

with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:

    snapshot = json.load(f)


apps = snapshot["apps"]
dependencies = snapshot["dependencies"]
models = snapshot["models"]
model_relationships = snapshot["model_relationships"]


# STEP 2 — Create graph

graph = nx.DiGraph()


# app nodes

for app in apps:

    graph.add_node(
        app,
        group="app"
    )


# app dependencies

for source, targets in dependencies.items():

    for target, weight in targets.items():

        graph.add_edge(
            source,
            target,
            label=f"imports ({weight})"
        )


# model nodes

for app, model_list in models.items():

    for model in model_list:

        graph.add_node(
            model,
            group="model"
        )

        # connect model to app

        graph.add_edge(
            app,
            model,
            label="contains"
        )


# model relationships

for source_model, relations in model_relationships.items():

    for relation in relations:

        target = relation["target"]
        relation_type = relation["type"]

        graph.add_edge(
            source_model,
            target,
            label=relation_type
        )


# STEP 3 — Build visualization

net = Network(
    height="900px",
    width="100%",
    directed=True
)


net.from_nx(graph)


# STEP 4 — Improve node appearance


for node in net.nodes:

    group = node.get("group")

    if group == "app":

        node["shape"] = "box"
        node["size"] = 30

    elif group == "model":

        node["shape"] = "dot"
        node["size"] = 18


# STEP 5 — Physics settings

net.set_options("""
{
  "physics": {
    "enabled": true,
    "barnesHut": {
      "gravitationalConstant": -2500,
      "springLength": 180
    }
  }
}
""")


# STEP 6 — Save graph

output_file = Path(
    "outputs/html/architecture_graph.html"
)

net.save_graph(str(output_file))


print(
    f"\\nArchitecture graph saved to: {output_file}"
)