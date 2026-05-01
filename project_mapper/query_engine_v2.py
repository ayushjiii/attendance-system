from architecture_engine import (
    ArchitectureEngine
)


engine = ArchitectureEngine()



# QUERY ROUTER


def handle_query(query):

    query = query.lower()


    
    # CENTRAL APPS
    

    if "central" in query:

        results = engine.get_central_apps()

        print("\nCENTRAL APPS:\n")


        for app, score in results:

            print(
                f"{app} "
                f"(score={score})"
            )


    
    # IMPACT ANALYSIS
    

    elif "impact" in query:

        words = query.split()


        target = words[-1]


        results = engine.analyze_impact(
            target
        )


        print(
            f"\nIMPACT OF {target}:\n"
        )


        if results:

            for item in results:

                print("-", item)

        else:

            print("No impact found")


    
    # WORKFLOW ANALYSIS
    

    elif "workflow" in query:

        words = query.split()

        keyword = words[-1]


        workflows = engine.find_workflow(
            keyword
        )


        print("\nWORKFLOWS:\n")


        if workflows:

            for workflow in workflows:

                print(
                    " → ".join(workflow)
                )

        else:

            print("No workflow found")


    
    # UNKNOWN QUERY
    

    else:

        print(
            "\nUnknown query"
        )



# INTERACTIVE LOOP


print("\nQUERY ENGINE\n")


while True:

    query = input(
        "\nAsk something: "
    )


    if query.lower() == "exit":

        break


    handle_query(query)