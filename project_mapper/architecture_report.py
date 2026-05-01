from pathlib import Path
import json
from collections import Counter


SNAPSHOT_FILE = Path("snapshots/snapshot.json")

REPORT_FILE = Path("reports/ARCHITECTURE_REPORT.md")


# STEP 1 — Load snapshot

with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:

    snapshot = json.load(f)


apps = snapshot["apps"]
dependencies = snapshot["dependencies"]
models = snapshot["models"]


# STEP 2 — Count dependencies

dependency_counter = Counter()

for source, targets in dependencies.items():

    dependency_counter[source] += len(targets)


# STEP 3 — Find most central app

most_central = None

if dependency_counter:

    most_central = dependency_counter.most_common(1)[0][0]


# STEP 4 — Find isolated apps

connected_apps = set()

for source, targets in dependencies.items():

    connected_apps.add(source)

    for target in targets:

        connected_apps.add(target)


isolated_apps = []

for app in apps:

    if app not in connected_apps:

        isolated_apps.append(app)


# STEP 5 — Build report

report = []


report.append("# Architecture Report\n")


# Apps

report.append("## Applications\n")

for app in apps:

    report.append(f"- {app}")

report.append("")


# Models

report.append("## Models\n")

for app, model_list in models.items():

    report.append(f"### {app}")

    for model in model_list:

        report.append(f"- {model}")

    report.append("")


# Dependencies

report.append("## Dependencies\n")

for source, targets in dependencies.items():

    for target in targets:

        report.append(
            f"- {source} ---> {target}"
        )

report.append("")


# Insights

report.append("## Architectural Insights\n")


if most_central:

    report.append(
        f"- Most central app: **{most_central}**"
    )


if isolated_apps:

    report.append(
        f"- Isolated apps: {', '.join(isolated_apps)}"
    )


# STEP 6 — Save report

with open(REPORT_FILE, "w", encoding="utf-8") as f:

    f.write("\n".join(report))


print(f"\nArchitecture report saved to: {REPORT_FILE}")