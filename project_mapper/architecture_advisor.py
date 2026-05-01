from pathlib import Path
import json


SNAPSHOT_FILE = Path(
    "snapshots/snapshot.json"
)


# STEP 1 — LOAD SNAPSHOT

with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:

    snapshot = json.load(f)


apps = snapshot["apps"]
dependencies = snapshot["dependencies"]
models = snapshot["models"]
relationships = snapshot["model_relationships"]



# STEP 2 — CENTRAL APP ANALYSIS

def find_central_apps():

    scores = {}


    for source, targets in dependencies.items():

        scores[source] = (
            scores.get(source, 0)
            + len(targets)
        )


        for target in targets:

            scores[target] = (
                scores.get(target, 0)
                + 1
            )


    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )


    return ranked



# STEP 3 — MODEL RELATIONSHIP ANALYSIS

def most_connected_models():

    model_scores = {}


    for model, relation_list in relationships.items():

        model_scores[model] = len(
            relation_list
        )


    ranked = sorted(
        model_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )


    return ranked



# STEP 4 — ISOLATED APPS


def find_isolated_apps():

    connected = set()


    for source, targets in dependencies.items():

        connected.add(source)

        for target in targets:

            connected.add(target)


    isolated = []


    for app in apps:

        if app not in connected:

            isolated.append(app)


    return isolated



# STEP 5 — GENERATE ADVISORY REPORT


print("\nARCHITECTURE ADVISOR\n")



# CENTRAL APPS


print("1. CENTRAL APPS\n")


central_apps = find_central_apps()


for app, score in central_apps[:5]:

    print(
        f"- {app} "
        f"(connectivity score={score})"
    )


if central_apps:

    top_app = central_apps[0][0]

    print(
        f"\nObservation: "
        f"{top_app} is becoming "
        f"a major coordination point."
    )



# MODEL ANALYSIS


print("\n2. MOST CONNECTED MODELS\n")


connected_models = most_connected_models()


for model, score in connected_models[:5]:

    print(
        f"- {model} "
        f"({score} relationships)"
    )



# ISOLATED APPS


print("\n3. ISOLATED APPS\n")


isolated = find_isolated_apps()


if isolated:

    for app in isolated:

        print(f"- {app}")


    print(
        "\nObservation: "
        "Isolated apps may indicate "
        "clean separation or unused modules."
    )

else:

    print("No isolated apps")



# COUPLING OBSERVATION

print("\n4. COUPLING OBSERVATIONS\n")


for source, targets in dependencies.items():

    weight = sum(targets.values())

    if weight >= 3:

        print(
            f"- {source} has elevated "
            f"dependency coupling "
            f"(weight={weight})"
        )


print("\nAnalysis complete.\n")