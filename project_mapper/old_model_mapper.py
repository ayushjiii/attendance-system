from pathlib import Path
import ast
import os

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


model_files = []


# STEP 1 — Find models.py files

for file in PROJECT_PATH.rglob("models.py"):

    skip = False

    for part in file.parts:

        if part in IGNORE_FOLDERS:
            skip = True
            break

    if not skip:
        model_files.append(file)


relationships = []


# STEP 2 — Parse models

for file in model_files:

    try:

        with open(file, "r", encoding="utf-8") as f:

            tree = ast.parse(f.read())

        # Find model classes

        for node in tree.body:

            if isinstance(node, ast.ClassDef):

                current_model = node.name

                # Find assignments inside model

                for item in node.body:

                    if isinstance(item, ast.Assign):

                        value = item.value

                        # Check for models.ForeignKey(...)

                        if isinstance(value, ast.Call):

                            func = value.func

                            if isinstance(func, ast.Attribute):

                                relation_type = func.attr

                                if relation_type in RELATION_FIELDS:

                                    if value.args:

                                        target = value.args[0]

                                        target_model = None


                                        # Case 1:
                                        # ForeignKey(Employee)

                                        if isinstance(target, ast.Name):

                                            target_model = target.id


                                        # Case 2:
                                        # ForeignKey("Employee")

                                        elif isinstance(target, ast.Constant):

                                            target_model = target.value


                                        # Case 3:
                                        # ForeignKey('accounts.Employee')

                                        elif isinstance(target, ast.Str):

                                            target_model = target.s


                                        # Save relationship if found

                                        if target_model:

                                            relationships.append(
                                                (
                                                    current_model,
                                                    target_model,
                                                    relation_type
                                                )
                                            )

    except Exception as e:

        print(f"\nERROR in {file}")
        print(e)


# STEP 3 — Print relationships

print("\nMODEL RELATIONSHIPS:\n")


for source, target, relation in relationships:

    print(
        f"{source} ---> {target} [{relation}]"
    )