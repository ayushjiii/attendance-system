from pathlib import Path
import json


SNAPSHOT_FILE = Path(
    "snapshots/snapshot.json"
)


# STEP 1 — Load snapshot

with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:

    snapshot = json.load(f)


apps = snapshot["apps"]
dependencies = snapshot["dependencies"]


print("\nARCHITECTURE SMELL REPORT\n")


# 1. GOD MODULE DETECTION

print("1. GOD MODULE CHECK\n")


GOD_THRESHOLD = 3


for app, targets in dependencies.items():

    dependency_count = len(targets)

    if dependency_count >= GOD_THRESHOLD:

        print(
            f"[WARNING] {app} imports "
            f"{dependency_count} apps"
        )


# 2. ISOLATED APP DETECTION


print("\n2. ISOLATED APPS\n")


connected_apps = set()


for source, targets in dependencies.items():

    connected_apps.add(source)

    for target in targets:

        connected_apps.add(target)


isolated_apps = []


for app in apps:

    if app not in connected_apps:

        isolated_apps.append(app)


if isolated_apps:

    for app in isolated_apps:

        print(f"[INFO] {app} is isolated")

else:

    print("No isolated apps found")


# 3. CIRCULAR DEPENDENCY DETECTION


print("\n3. CIRCULAR DEPENDENCIES\n")


found_cycle = False


for source, targets in dependencies.items():

    for target in targets:

        if target in dependencies:

            reverse_targets = dependencies[target]

            if source in reverse_targets:

                found_cycle = True

                print(
                    f"[WARNING] Circular dependency: "
                    f"{source} ↔ {target}"
                )


if not found_cycle:

    print("No circular dependencies found")


# 4. HIGH COUPLING CHECK
print("\n4. HIGH COUPLING CHECK\n")


for app, targets in dependencies.items():

    total_weight = sum(targets.values())

    if total_weight >= 4:

        print(
            f"[WARNING] {app} has high coupling "
            f"(weight={total_weight})"
        )


print("\nAnalysis complete.\n")