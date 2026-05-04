from pathlib import Path
import json
import os

#ignored folders

IGNORED_FOLDERS = {

    "venv",

    "__pycache__",

    ".git",

    "snapshots",

    "outputs",

    "node_modules"
}


SNAPSHOT_FILE = Path(
    "snapshots/snapshot.json"
)



# STEP 1 — LOAD SNAPSHOT


with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:

    snapshot = json.load(f)


python_files = snapshot["python_files"]



# STEP 2 — CONTEXT RETRIEVAL


def retrieve_context(keyword):

    keyword = keyword.lower()

    matched_files = []


    for file_path in python_files:

        full_path = PROJECT_ROOT / file_path


        try:

            with open(
                full_path,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read().lower()


            score = content.count(keyword)


            if score > 0:

                matched_files.append({

                    "file": file_path,
                    "score": score
                })


        except Exception:

            continue


    matched_files.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    return matched_files



# STEP 3 — INTERACTIVE LOOP


print("\nCONTEXT RETRIEVER\n")


while True:

    keyword = input(
        "\nKeyword (or exit): "
    )


    if keyword.lower() == "exit":

        break


    results = retrieve_context(keyword)


    if results:

        print("\nMOST RELEVANT FILES:\n")


        for item in results[:10]:

            print(
                f"{item['file']} "
                f"(score={item['score']})"
            )

    else:

        print("\nNo matching files found")