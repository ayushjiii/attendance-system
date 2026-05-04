from pathlib import Path
import json
from collections import defaultdict
from pyvis.network import Network



# FILES


SNAPSHOT_FILE = Path(
    "snapshots/snapshot.json"
)

CALL_GRAPH_FILE = Path(
    "snapshots/hybrid/filtered_call_graph.json"
)

OUTPUT_FILE = (
    "outputs/html/human_architecture_graph.html"
)



# LOAD SNAPSHOT


with open(
    SNAPSHOT_FILE,
    "r",
    encoding="utf-8"
) as f:

    snapshot = json.load(f)


apps = snapshot["apps"]
models = snapshot["models"]
dependencies = snapshot["dependencies"]

relationships = snapshot.get(
    "model_relationships",
    {}
)

# load hybrid grapph

with open(
    CALL_GRAPH_FILE,
    "r",
    encoding="utf-8"
) as f:

    call_graph = json.load(f)

#important function nodes

function_scores = []


for caller, callees in call_graph.items():

    score = len(set(callees))

    function_scores.append(
        (caller, score)
    )


function_scores.sort(
    key=lambda x: x[1],
    reverse=True
)


## adjust it according to how many function you want to see 

TOP_FUNCTIONS = 50


important_functions = set()


for func, score in function_scores[
    :TOP_FUNCTIONS
]:

    important_functions.add(func)


#create network

net = Network(
    height="900px",
    width="100%",
    directed=True,
    bgcolor="#f5f5f5",
    font_color="black"
)


# COMPACT PHYSICS SETTINGS


net.barnes_hut(
    gravity=-50000,
    central_gravity=0.9,
    spring_length=110,
    spring_strength=0.02,
    damping=0.09
)

net.set_options("""
var options = {
  "layout": {
    "improvedLayout": true
  },
  "physics": {
    "solver": "barnesHut",
    "barnesHut": {
      "gravitationalConstant": -5000,
      "centralGravity": 0.9,
      "springLength": 110,
      "springConstant": 0.02,
      "damping": 0.09
    },
    "minVelocity": 0.75
  }
}
""")




# TRACKERS


added_nodes = set()



# APP NODES


for app in apps:

    net.add_node(
        app,
        label=app,
        shape="box",
        size=35,
        color="#6FA8DC"
    )

    added_nodes.add(app)



# MODEL NODES


for app_name, app_models in models.items():

    for model in app_models:


        if model not in added_nodes:

            net.add_node(
                model,
                label=model,
                shape="dot",
                size=20,
                color="#FFD966"
            )

            added_nodes.add(model)


        net.add_edge(
            app_name,
            model,
            label="contains"
        )



# APP DEPENDENCIES

for source, targets in dependencies.items():

    for target in targets:

        net.add_edge(
            source,
            target,
            label="imports"
        )



# MODEL RELATIONSHIPS


for model, relations in relationships.items():

    for relation in relations:


        target = relation["target"]

        relation_type = relation["type"]


        if target not in added_nodes:

            net.add_node(
                target,
                label=target,
                shape="dot",
                size=15,
                color="#F6B26B"
            )

            added_nodes.add(target)


        net.add_edge(
            model,
            target,
            label=relation_type,
            color="orange"
        )




# IMPORTANT FUNCTION NODES


for function_name in important_functions:


    if function_name not in added_nodes:

        net.add_node(
            function_name,
            label=function_name,
            shape="diamond",
            size=18,
            color="#93C47D"
        )

        added_nodes.add(function_name)



# FUNCTION CONNECTIONS


for caller, callees in call_graph.items():

    if caller not in important_functions:

        continue


    for callee in callees:


        if callee not in important_functions:

            continue


        net.add_edge(
            caller,
            callee,
            color="green"
        )



# SAVE


net.write_html(
    OUTPUT_FILE,
    notebook=False
)


print(
    "\nINTERACTIVE HUMAN ARCHITECTURE GRAPH CREATED\n"
)