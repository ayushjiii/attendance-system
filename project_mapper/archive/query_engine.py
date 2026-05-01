from pathlib import Path
import json


SNAPSHOT_FILE = Path(
    "snapshots/snapshot.json"
)


## load snapshot


with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:

    snapshot = json.load(f)


dependencies = snapshot["dependencies"]
models = snapshot["models"]
relationships = snapshot["model_relationships"]


## find app dependents

def find_dependents(app_name):

    results = []

    for source, targets in dependencies.items():

        if app_name in targets:

            results.append(source)

    return results


## models in app

def get_models(app_name):

    return models.get(app_name, [])


## model relationship

def get_relationships(model_name):

    return relationships.get(model_name, [])


## most connected model

def most_connected_model():

    highest_model = None
    highest_count = 0

    for model, relations in relationships.items():

        relation_count = len(relations)

        if relation_count > highest_count:

            highest_count = relation_count
            highest_model = model

    return highest_model, highest_count


# menu

print("\nARCHITECTURE QUERY ENGINE\n")


while True:

    print("\nOPTIONS:")
    print("1. Find app dependents")
    print("2. Get models in app")
    print("3. Get model relationships")
    print("4. Most connected model")
    print("5. Exit")


    choice = input("\nEnter choice: ")


    if choice == "1":

        app = input("Enter app name: ")

        results = find_dependents(app)

        if results:

            print("\nDependent apps:")

            for item in results:

                print(f"- {item}")

        else:

            print("\nNo dependents found")


    elif choice == "2":

        app = input("Enter app name: ")

        result = get_models(app)

        if result:

            print("\nModels:")

            for model in result:

                print(f"- {model}")

        else:

            print("\nNo models found")



    elif choice == "3":

        model = input("Enter model name: ")

        result = get_relationships(model)

        if result:

            print("\nRelationships:")

            for relation in result:

                print(
                    f"- {relation['type']} "
                    f"-> {relation['target']}"
                )

        else:

            print("\nNo relationships found")


    

    elif choice == "4":

        model, count = most_connected_model()

        print(
            f"\nMost connected model: "
            f"{model} ({count} relationships)"
        )




    elif choice == "5":

        print("\nExiting query engine.\n")
        break



    else:

        print("\nInvalid choice")