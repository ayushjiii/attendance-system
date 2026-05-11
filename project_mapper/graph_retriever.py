from pathlib import Path
import json


GRAPH_FILE = Path(
    "snapshots/hybrid/filtered_call_graph.json"
)


with open(
    GRAPH_FILE,
    "r",
    encoding="utf-8"
) as f:

    graph = json.load(f)


def graph_search(query, max_connections=10):

    q = query.lower()

    matched_nodes = []

    connected_nodes = set()

    results = []


    # MATCH ROOT NODES

    for node in graph:

        if q in node.lower():

            matched_nodes.append(node)


    # TRAVERSE CONNECTIONS

    for node in matched_nodes:

        connected_nodes.add(node)

        for callee in graph.get(node, []):

            connected_nodes.add(callee)

            if len(connected_nodes) >= max_connections:
                break


    # FORMAT RESULTS

    for node in connected_nodes:

        connections = graph.get(node, [])

        code_preview = "\n".join(
            [f"calls -> {c}" for c in connections[:5]]
        )

        results.append({

            "chunk": {

                "name": node,

                "file": "graph_relation",

                "code": code_preview
            }

        })

    return results