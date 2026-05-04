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
    "snapshots/raw/model_usage.json"
)



# RESULTS

model_usage = {}


# FUNCTION MODEL VISITOR

class FunctionModelVisitor(ast.NodeVisitor):


    def __init__(self):

        self.current_function = None


    
    # FUNCTION DETECTION
    

    def visit_FunctionDef(self, node):


        self.current_function = node.name


        if self.current_function not in model_usage:

            model_usage[self.current_function] = []


        self.generic_visit(node)


    
    # ORM CALL DETECTION
    

    def visit_Call(self, node):


        """
        Detect patterns like:

        AttendanceRecord.objects.filter()
        Employee.objects.all()
        """


        try:

            func = node.func


            # METHOD CALL

            if isinstance(func, ast.Attribute):


                objects_attr = func.value


                # .objects
                

                if isinstance(objects_attr, ast.Attribute):


                    if objects_attr.attr == "objects":


                        model_node = objects_attr.value


                        
                        # MODEL NAME
                        

                        if isinstance(

                            model_node,

                            ast.Name

                        ):


                            model_name = model_node.id


                            
                            # SIMPLE MODEL HEURISTIC
                            

                            if model_name[0].isupper():


                                if (

                                    self.current_function
                                    and
                                    model_name
                                    not in
                                    model_usage[
                                        self.current_function
                                    ]

                                ):


                                    model_usage[
                                        self.current_function
                                    ].append(model_name)


        except Exception:

            pass


        self.generic_visit(node)



# SCAN PYTHON FILES

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


    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            source_code = f.read()


        tree = ast.parse(source_code)


        visitor = FunctionModelVisitor()

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
        model_usage,
        f,
        indent=4
    )



# DONE


print(
    "\nMODEL USAGE GRAPH CREATED\n"
)