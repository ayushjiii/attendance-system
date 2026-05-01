from architecture_engine import ArchitectureEngine


engine = ArchitectureEngine()


print("\nCENTRAL APPS:\n")

for app, score in engine.get_central_apps():

    print(app, score)


print("\nIMPACT:\n")

print(
    engine.analyze_impact(
        "reports"
    )
)


print("\nWORKFLOWS:\n")

print(
    engine.find_workflow(
        "leave"
    )
)