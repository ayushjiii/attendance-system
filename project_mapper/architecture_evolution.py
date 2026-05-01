from pathlib import Path
import json


OLD_SNAPSHOT = Path(
    "history/snapshot_2026_04_28__16_53_24.json"
)

NEW_SNAPSHOT = Path(
    "snapshots/snapshot.json"
)


# STEP 1 — LOAD SNAPSHOTS

with open(OLD_SNAPSHOT, "r", encoding="utf-8") as f:

    old_snapshot = json.load(f)


with open(NEW_SNAPSHOT, "r", encoding="utf-8") as f:

    new_snapshot = json.load(f)


# STEP 2 — EXTRACT DATA

old_dependencies = old_snapshot["dependencies"]
new_dependencies = new_snapshot["dependencies"]


old_models = old_snapshot["models"]
new_models = new_snapshot["models"]


# STEP 3 — FIND NEW DEPENDENCIES

new_edges = []


for source, targets in new_dependencies.items():

    old_targets = old_dependencies.get(
        source,
        []
    )


    for target in targets:

        if target not in old_targets:

            new_edges.append(
                (source, target)
            )



# STEP 4 — FIND REMOVED DEPENDENCIES


removed_edges = []


for source, targets in old_dependencies.items():

    new_targets = new_dependencies.get(
        source,
        []
    )


    for target in targets:

        if target not in new_targets:

            removed_edges.append(
                (source, target)
            )



# STEP 5 — FIND NEW MODELS


new_model_entries = []


for app, model_list in new_models.items():

    old_model_list = old_models.get(
        app,
        []
    )


    for model in model_list:

        if model not in old_model_list:

            new_model_entries.append(
                (app, model)
            )



# STEP 6 — REPORT


print("\nARCHITECTURE EVOLUTION REPORT\n")



# NEW DEPENDENCIES


print("1. NEW DEPENDENCIES\n")


if new_edges:

    for source, target in new_edges:

        print(
            f"- {source} → {target}"
        )

else:

    print("No new dependencies")


# removed dependencies

print("\n2. REMOVED DEPENDENCIES\n")


if removed_edges:

    for source, target in removed_edges:

        print(
            f"- {source} → {target}"
        )

else:

    print("No removed dependencies")

# new models

print("\n3. NEW MODELS\n")


if new_model_entries:

    for app, model in new_model_entries:

        print(
            f"- {model} added to {app}"
        )

else:

    print("No new models")

# summary

print("\n4. EVOLUTION SUMMARY\n")


print(
    f"New dependencies: "
    f"{len(new_edges)}"
)

print(
    f"Removed dependencies: "
    f"{len(removed_edges)}"
)

print(
    f"New models: "
    f"{len(new_model_entries)}"
)


print("\nAnalysis complete.\n")