from pathlib import Path
import ast
import json
import os

# ignored folders
PROJECT_ROOT = Path(
    "../"
).resolve()


IGNORED_FOLDERS = {

    "venv",

    "__pycache__",

    ".git",

    "snapshots",

    "outputs",

    "node_modules"
}



# STORAGE


function_map = {}



# PROCESS FILES


python_files = []


for root, dirs, files in os.walk(PROJECT_ROOT):


    # REMOVE IGNORED DIRECTORIES

    dirs[:] = [

        d for d in dirs

        if d not in IGNORED_FOLDERS
    ]

    for file in files:


        if file.endswith(".py"):


            python_files.append(

                Path(root) / file
            )

for file_path in python_files:

    relative_path = str(
        file_path.relative_to(
            PROJECT_ROOT
        )
    )


    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            source_code = f.read()


        tree = ast.parse(source_code)


    except Exception:

        continue


    
    # FILE STRUCTURE
   

    file_data = {
        "functions": [],
        "classes": {}
    }


    
    # ONLY TOP-LEVEL NODES
    

    for node in tree.body:


        
        # TOP-LEVEL FUNCTIONS
        

        if isinstance(node, ast.FunctionDef):

            file_data[
                "functions"
            ].append(
                node.name
            )


        
        # CLASSES
        

        elif isinstance(node, ast.ClassDef):

            methods = []


            
            # CLASS BODY ONLY
            

            for item in node.body:

                if isinstance(
                    item,
                    ast.FunctionDef
                ):

                    methods.append(
                        item.name
                    )


            file_data[
                "classes"
            ][node.name] = methods


   
    # SAVE FILE DATA
    

    function_map[
        relative_path
    ] = file_data



# SAVE JSON


OUTPUT_FILE = Path(
    "snapshots/raw/detailed_function_map.json"
)


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        function_map,
        f,
        indent=4
    )


print("\nFUNCTION MAP CREATED\n")

print(
    f"Files analyzed: "
    f"{len(function_map)}"
)