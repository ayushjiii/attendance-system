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



# OUTPUT FILE


OUTPUT_FILE = Path(
    "snapshots/raw/code_chunks.json"
)



# RESULTS


code_chunks = {}


# CHUNK VISITOR

class CodeChunkVisitor(ast.NodeVisitor):


    def __init__(

        self,

        source_code,

        file_path

    ):


        self.source_code = source_code

        self.file_path = str(file_path)


    
    # FUNCTION CHUNKS
    

    def visit_FunctionDef(self, node):


        function_name = node.name


        chunk = ast.get_source_segment(

            self.source_code,

            node

        )


        code_chunks[function_name] = {

            "type": "function",

            "file": self.file_path,

            "start_line": node.lineno,

            "end_line": node.end_lineno,

            "code": chunk
        }


        self.generic_visit(node)


    
    # CLASS CHUNKS
    

    def visit_ClassDef(self, node):


        class_name = node.name


        chunk = ast.get_source_segment(

            self.source_code,

            node

        )


        code_chunks[class_name] = {

            "type": "class",

            "file": self.file_path,

            "start_line": node.lineno,

            "end_line": node.end_lineno,

            "code": chunk
        }


        self.generic_visit(node)



# SCAN FILES


python_files = []


for root, dirs, files in os.walk(PROJECT_ROOT):


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


    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            source_code = f.read()


        tree = ast.parse(source_code)


        visitor = CodeChunkVisitor(

            source_code,

            file_path

        )


        visitor.visit(tree)


    except Exception as e:

        print(f"\nERROR: {file_path}")
        print(e)



# SAVE JSON


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(

        code_chunks,

        f,

        indent=4
    )



# DONE


print(
    "\nCODE CHUNKS CREATED\n"
)