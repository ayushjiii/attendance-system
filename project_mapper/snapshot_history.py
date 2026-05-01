from pathlib import Path
import json
import shutil
from datetime import datetime


SNAPSHOT_FILE = Path(
    "snapshots/snapshot.json"
)

HISTORY_FOLDER = Path(
    "history"
)


# STEP 1 — Ensure history folder exists

HISTORY_FOLDER.mkdir(exist_ok=True)


# STEP 2 — Create timestamped filename

timestamp = datetime.now().strftime(
    "%Y_%m_%d__%H_%M_%S"
)

history_file = HISTORY_FOLDER / (
    f"snapshot_{timestamp}.json"
)


# STEP 3 — Save historical snapshot

shutil.copy(
    SNAPSHOT_FILE,
    history_file
)


print(
    f"\nSnapshot archived: {history_file}"
)


# STEP 4 — Compare latest two snapshots


history_files = sorted(
    HISTORY_FOLDER.glob("snapshot_*.json")
)


if len(history_files) < 2:

    print(
        "\nNot enough snapshots for comparison."
    )

    exit()


latest = history_files[-1]
previous = history_files[-2]


print("\nCOMPARING SNAPSHOTS\n")

print(f"Previous: {previous.name}")
print(f"Latest:   {latest.name}")


# STEP 5 — Load snapshots

with open(previous, "r", encoding="utf-8") as f:

    old_snapshot = json.load(f)


with open(latest, "r", encoding="utf-8") as f:

    new_snapshot = json.load(f)



# STEP 6 — Compare apps


print("\n1. APP CHANGES\n")


old_apps = set(old_snapshot["apps"])
new_apps = set(new_snapshot["apps"])


added_apps = new_apps - old_apps
removed_apps = old_apps - new_apps


if added_apps:

    for app in added_apps:

        print(f"[ADDED] App: {app}")


if removed_apps:

    for app in removed_apps:

        print(f"[REMOVED] App: {app}")


if not added_apps and not removed_apps:

    print("No app changes")



# STEP 7 — Compare dependencies


print("\n2. DEPENDENCY CHANGES\n")


old_dependencies = old_snapshot["dependencies"]
new_dependencies = new_snapshot["dependencies"]


for app in new_dependencies:

    old_targets = set(
        old_dependencies.get(app, {}).keys()
    )

    new_targets = set(
        new_dependencies.get(app, {}).keys()
    )


    added = new_targets - old_targets
    removed = old_targets - new_targets


    for target in added:

        print(
            f"[NEW DEPENDENCY] "
            f"{app} ---> {target}"
        )


    for target in removed:

        print(
            f"[REMOVED DEPENDENCY] "
            f"{app} ---> {target}"
        )



# STEP 8 — Compare models


print("\n3. MODEL CHANGES\n")


old_models = old_snapshot["models"]
new_models = new_snapshot["models"]


for app in new_models:

    old_model_set = set(
        old_models.get(app, [])
    )

    new_model_set = set(
        new_models.get(app, [])
    )


    added_models = (
        new_model_set - old_model_set
    )

    removed_models = (
        old_model_set - new_model_set
    )


    for model in added_models:

        print(
            f"[NEW MODEL] {app}.{model}"
        )


    for model in removed_models:

        print(
            f"[REMOVED MODEL] {app}.{model}"
        )


print("\nComparison complete.\n")