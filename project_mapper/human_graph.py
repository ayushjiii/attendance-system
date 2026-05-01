from pathlib import Path
import json
from collections import defaultdict



# FILES


INPUT_FILE = Path(
    "snapshots/raw/detailed_call_graph.json"
)

OUTPUT_FILE = Path(
    "snapshots/human/simplified_call_graph.json"
)



# SETTINGS


MIN_OUTGOING_CALLS = 5
MAX_FUNCTIONS = 20



# LOAD GRAPH


with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    call_graph = json.load(f)


# COUNT INCOMING CALLS


incoming_counts = defaultdict(int)


for caller, callees in call_graph.items():

    for callee in set(callees):

        incoming_counts[callee] += 1


# FIND EXTERNAL / ORCHESTRATOR FUNCTIONS

candidate_functions = []


for caller, callees in call_graph.items():

    unique_callees = set(callees)

    outgoing = len(unique_callees)

    incoming = incoming_counts[caller]


    # HUMAN-IMPORTANT FUNCTIONS

    # High outgoing calls
    # Low incoming calls
    # Means:
    # top-level orchestrator / workflow function

    if (
        outgoing >= MIN_OUTGOING_CALLS
        and incoming <= 2
    ):

        candidate_functions.append(
            (
                caller,
                outgoing
            )
        )



# SORT BY IMPORTANCE


candidate_functions.sort(
    key=lambda x: x[1],
    reverse=True
)



# KEEP TOP FUNCTIONS


top_functions = set()


for func, score in candidate_functions[
    :MAX_FUNCTIONS
]:

    top_functions.add(func)


# build human graph
human_graph = {}


for caller, callees in call_graph.items():

    if caller not in top_functions:

        continue


    filtered_callees = []


    for callee in callees:

        if callee in top_functions:

            filtered_callees.append(callee)


    filtered_callees = sorted(
        list(set(filtered_callees))
    )


    if filtered_callees:

        human_graph[
            caller
        ] = filtered_callees



with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        human_graph,
        f,
        indent=4
    )


print(
    "\nARCHITECTURE-LEVEL HUMAN GRAPH CREATED\n"
)

print(
    f"Functions kept: "
    f"{len(human_graph)}"
)