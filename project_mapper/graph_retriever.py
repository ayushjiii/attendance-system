import json
from collections import deque
from pathlib import Path


# =========================================================
# LOAD GRAPH
# =========================================================

GRAPH_FILE = Path(
    "snapshots/unified/unified_graph.json"
)

with open(
    GRAPH_FILE,
    "r",
    encoding="utf-8"
) as f:

    graph = json.load(f)


nodes = graph["nodes"]

edges = graph["edges"]


# =========================================================
# BUILD ADJACENCY
# =========================================================

adjacency = {}

for edge in edges:

    source = edge["source"]

    if source not in adjacency:

        adjacency[source] = []

    adjacency[source].append({

        "target": edge["target"],

        "relation": edge["relation"]
    })


# =========================================================
# SEARCH MATCHES
# =========================================================

def find_start_nodes(query):

    q = query.lower()

    scored = []

    for node_id, data in nodes.items():

        score = 0

        node_lower = node_id.lower()

        file_lower = data["file"].lower()

        type_lower = data["type"].lower()

        # =================================================
        # DIRECT NODE MATCH
        # =================================================

        for word in q.split():

            if word in node_lower:

                score += 10

            if word in file_lower:

                score += 4

            if word == type_lower:

                score += 6

        # =================================================
        # IMPORTANT TYPE BOOSTS
        # =================================================

        if "workflow" in q:

            if type_lower in [

                "view",
                "function",
                "model"

            ]:

                score += 8

        if "dependency" in q or "break" in q:

            if type_lower in [

                "model",
                "view"

            ]:

                score += 10

        if "attendance" in q:

            if "attendance" in node_lower:

                score += 20

            if "attendance" in file_lower:

                score += 12

        # =================================================
        # NOISE PENALTY
        # =================================================

        noise_words = [

            "builder",
            "mapper",
            "helper",
            "utils",
            "__init__"

        ]

        for noise in noise_words:

            if noise in node_lower:

                score -= 15

        # =================================================
        # KEEP
        # =================================================

        if score > 0:

            scored.append(

                (
                    score,
                    node_id
                )
            )

    scored.sort(reverse=True)

    return [

        node

        for _, node in scored[:10]
    ]


# =========================================================
# BFS TRAVERSAL
# =========================================================

def bfs_paths(start_node, max_depth=4):

    queue = deque()

    queue.append(

        (
            start_node,
            [],
            0
        )
    )

    visited = set()

    results = []

    while queue:

        current, path, depth = queue.popleft()

        if depth > max_depth:

            continue

        if current in visited:

            continue

        visited.add(current)

        neighbors = adjacency.get(current, [])

        for neighbor in neighbors:

            nxt = neighbor["target"]

            relation = neighbor["relation"]

            step = {

                "from": current,

                "relation": relation,

                "to": nxt
            }

            new_path = path + [step]

            results.append(new_path)

            queue.append(

                (
                    nxt,
                    new_path,
                    depth + 1
                )
            )

    return results


# =========================================================
# GRAPH SEARCH
# =========================================================

def graph_search(query):

    matched_nodes = find_start_nodes(query)

    results = []

    for node in matched_nodes[:5]:

        paths = bfs_paths(node)

        for path in paths[:10]:

            formatted = []

            for step in path:

                formatted.append(

                    f"{step['from']}"
                    f"\n--[{step['relation']}]-->\n"
                    f"{step['to']}"
                )

            formatted_text = "\n\n".join(formatted)

            results.append({

                "chunk": {

                    "name": node,

                    "file": nodes.get(
                        node,
                        {}
                    ).get(
                        "file",
                        ""
                    ),

                    "code": formatted_text
                }
            })

    return results


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    while True:

        q = input("\nQuery: ")

        if q == "exit":

            break

        results = graph_search(q)

        print("\nRESULTS\n")

        for r in results:

            print("=" * 50)

            print(r["chunk"]["code"])