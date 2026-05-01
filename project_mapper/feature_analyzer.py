from pathlib import Path
import json


SNAPSHOT_FILE = Path(
    "snapshots/snapshot.json"
)


# STEP 1 — LOAD SNAPSHOT


with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:

    snapshot = json.load(f)


apps = snapshot["apps"]
models = snapshot["models"]
dependencies = snapshot["dependencies"]


# STEP 2 — FEATURE ANALYSIS


def analyze_feature(feature_name):

    feature_name = feature_name.lower()


    matched_apps = []
    matched_models = []
    connected_apps = set()

# search apps

    for app in apps:

        if feature_name in app.lower():

            matched_apps.append(app)


    # search models

    for app, model_list in models.items():

        for model in model_list:

            if feature_name in model.lower():

                matched_models.append(model)

                connected_apps.add(app)


    #  FIND CONNECTED DEPENDENCIES

    for source, targets in dependencies.items():

        if source in matched_apps:

            for target in targets:

                connected_apps.add(target)


        for target in targets:

            if target in matched_apps:

                connected_apps.add(source)


    return {
        "apps": matched_apps,
        "models": matched_models,
        "connected_apps": list(connected_apps)
    }


# STEP 3 — INTERACTIVE LOOP

print("\nFEATURE ANALYZER\n")


while True:

    feature = input(
        "\nFeature name (or exit): "
    )


    if feature.lower() == "exit":

        break


    result = analyze_feature(feature)


    print("\nMATCHED APPS:\n")

    if result["apps"]:

        for app in result["apps"]:

            print(f"- {app}")

    else:

        print("None")


    print("\nMATCHED MODELS:\n")

    if result["models"]:

        for model in result["models"]:

            print(f"- {model}")

    else:

        print("None")


    print("\nCONNECTED APPS:\n")

    if result["connected_apps"]:

        for app in result["connected_apps"]:

            print(f"- {app}")

    else:

        print("None")