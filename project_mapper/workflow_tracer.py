from pathlib import Path
import json


# FILES

CALL_GRAPH_FILE = Path(
    "snapshots/hybrid/filtered_call_graph.json"
)



# LOAD GRAPH


with open(
    CALL_GRAPH_FILE,
    "r",
    encoding="utf-8"
) as f:

    call_graph = json.load(f)


# DFS WORKFLOW TRACER

def trace_workflow(


    function_name,

    visited=None,

    depth=0
):


    
    # INITIALIZE VISITED
    

    if visited is None:

        visited = set()


    
    # AVOID INFINITE LOOPS
    

    if function_name in visited:

        return


    visited.add(function_name)


    
    # PRINT CURRENT FUNCTION
    

    indent = "    " * depth

    print(f"{indent}- {function_name}")


    
    # GET NEXT FUNCTIONS
    

    next_functions = call_graph.get(
        function_name,
        []
    )

    print(next_functions)


    # RECURSIVE DFS
    

    for next_function in next_functions:

        trace_workflow(

            next_function,

            visited,

            depth + 1
        )


# MENU


print("\nWORKFLOW TRACER\n")


while True:


    start_function = input(

        "\nEnter function name "
        "(or 'exit'): "

    )


    if start_function.lower() == "exit":

        break


    print("\nWORKFLOW:\n")


    trace_workflow(start_function)