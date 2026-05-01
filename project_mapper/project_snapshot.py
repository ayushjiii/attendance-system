from pathlib import Path
import ast
import json
from collections import defaultdict
from datetime import datetime


PROJECT_PATH = Path(r"E:\WORK\python\ATTENDENCE")


IGNORE_FOLDERS = {
    "__pycache__",
    ".git",
    "venv",
    "env",
    "node_modules",
    "migrations"
}

RELATION_FIELDS = {
    "ForeignKey",
    "OneToOneField",
    "ManyToManyField"
}

snapshot = {
    "generated_at": datetime.now().isoformat(),
    "apps": [],
    "python_files": [],
    "dependencies": {},
    "models": {},
    "model_relationships": {}
}


python_files = []


# STEP 1 — Detect REAL Django apps only

PROJECT_APPS = set()

for item in PROJECT_PATH.iterdir():

    if item.is_dir():

        if item.name not in IGNORE_FOLDERS:

            apps_file = item / "apps.py"

            if apps_file.exists():

                PROJECT_APPS.add(item.name)

                snapshot["apps"].append(item.name)


# STEP 2 — Collect python files

for file in PROJECT_PATH.rglob("*.py"):

    skip = False

    for part in file.parts:

        if part in IGNORE_FOLDERS:

            skip = True
            break

    if not skip:

        python_files.append(file)

        snapshot["python_files"].append(
            str(file.relative_to(PROJECT_PATH))
        )


# STEP 3 — Dependency storage

dependency_counter = defaultdict(
    lambda: defaultdict(int)
)


# STEP 4 — Analyze files

for file in python_files:

    try:

        with open(file, "r", encoding="utf-8") as f:

            tree = ast.parse(f.read())

        current_app = file.parts[-2]


        # ---------- IMPORT ANALYSIS ----------

        for node in ast.walk(tree):

            if isinstance(node, ast.ImportFrom):

                module = node.module

                if module:

                    imported_app = module.split(".")[0]

                    if imported_app in PROJECT_APPS:

                        if imported_app != current_app:

                            dependency_counter[
                                current_app
                            ][imported_app] += 1


        # ---------- MODEL ANALYSIS ----------

        if file.name == "models.py":

            snapshot["models"][current_app] = []

            for node in tree.body:

                if isinstance(node, ast.ClassDef):

                    current_model = node.name

                    snapshot["models"][
                        current_app
                    ].append(current_model)

                    snapshot["model_relationships"][
                        current_model
                    ] = []

                    # Analyze fields

                    for item in node.body:

                        if isinstance(item, ast.Assign):

                            value = item.value

                            if isinstance(value, ast.Call):

                                func = value.func

                                if isinstance(func, ast.Attribute):

                                    relation_type = func.attr

                                    if relation_type in RELATION_FIELDS:

                                        if value.args:

                                            target = value.args[0]

                                            target_model = None


                                            # ForeignKey(Employee)

                                            if isinstance(target, ast.Name):

                                                target_model = target.id


                                            # ForeignKey("Employee")

                                            elif isinstance(target, ast.Constant):

                                                target_model = str(
                                                    target.value
                                                )


                                            # ForeignKey(settings.AUTH_USER_MODEL)

                                            else:

                                                try:

                                                    target_model = ast.unparse(
                                                        target
                                                    )

                                                except:

                                                    pass


                                                if target_model:

                                                    snapshot[
                                                        "model_relationships"
                                                    ][current_model].append(
                                                        {
                                                            "target": target_model,
                                                            "type": relation_type
                                                        }
                                                    )

    except Exception as e:

        print(f"\nERROR in {file}")
        print(e)


# STEP 5 — Convert dependencies

for source, targets in dependency_counter.items():

    snapshot["dependencies"][source] = dict(targets)


# STEP 6 — Save snapshot

output_file = Path("snapshots/snapshot.json")

with open(output_file, "w", encoding="utf-8") as f:

    json.dump(snapshot, f, indent=4)


print(f"\nSnapshot saved to: {output_file}")