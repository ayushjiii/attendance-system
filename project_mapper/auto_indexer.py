import os
import json
import hashlib
import ast

from datetime import datetime

# =========================================
# CONFIG
# =========================================

PROJECT_PATH = r"E:\WORK\python\ATTENDENCE"

INDEX_FILE = "project_index.json"
STATE_FILE = "file_state.json"

IGNORE_FOLDERS = {
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
    "migrations",

    # RAG junk folders
    "outputs",
    "snapshots",
    "history",
    "archive",
    "lib"
}

IGNORE_FILES = {
    "project_index.json",
    "file_state.json",
    "llm_cache.json",
    "rag_log.json"
}

ALLOWED_EXTENSIONS = {
    ".py",
    ".html",
    ".css",
    ".js",
    ".json",
    ".txt",
    ".md"
}

CHUNK_SIZE = 1200

# =========================================
# LOAD OLD STATE
# =========================================

if os.path.exists(STATE_FILE):

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        old_state = json.load(f)

else:
    old_state = {}

# =========================================
# HELPERS
# =========================================

def get_file_hash(filepath):

    with open(filepath, "rb") as f:

        file_data = f.read()

    return hashlib.md5(file_data).hexdigest()


def read_file_content(filepath):

    try:

        with open(filepath, "r", encoding="utf-8") as f:

            return f.read()

    except:

        return ""


def create_chunks(content):

    chunks = []

    start = 0

    while start < len(content):

        end = start + CHUNK_SIZE

        chunk = content[start:end]

        chunks.append(chunk)

        start = end

    return chunks


# =========================================
# METADATA EXTRACTION
# =========================================

def extract_python_metadata(content):

    metadata = {
        "functions": [],
        "classes": [],
        "imports": [],
        "models_used": [],
        "templates_used": []
    }

    try:

        tree = ast.parse(content)

        for node in ast.walk(tree):

            # Functions
            if isinstance(node, ast.FunctionDef):

                metadata["functions"].append(node.name)

            # Classes
            elif isinstance(node, ast.ClassDef):

                metadata["classes"].append(node.name)

            # Imports
            elif isinstance(node, ast.Import):

                for alias in node.names:

                    metadata["imports"].append(alias.name)

            elif isinstance(node, ast.ImportFrom):

                if node.module:

                    metadata["imports"].append(node.module)

            # Detect render templates
            elif isinstance(node, ast.Call):

                try:

                    if hasattr(node.func, "id"):

                        if node.func.id == "render":

                            if len(node.args) >= 3:

                                template_arg = node.args[2]

                                if isinstance(template_arg, ast.Constant):

                                    metadata["templates_used"].append(
                                        template_arg.value
                                    )

                except:
                    pass

        # Detect models used
        for model in [
            "AttendanceRecord",
            "Employee",
            "LeaveRequest",
            "Holiday"
        ]:

            if model in content:

                metadata["models_used"].append(model)

    except:

        pass

    return metadata


def detect_module(filepath):

    parts = filepath.split(os.sep)

    for folder in [
        "accounts",
        "attendance",
        "holidays",
        "leave_management",
        "reports",
        "attendance_system",
        "project_mapper"
    ]:

        if folder in parts:

            return folder

    return "unknown"


def detect_file_type(filepath):

    filename = os.path.basename(filepath)

    if filename == "views.py":
        return "django_view"

    elif filename == "models.py":
        return "django_model"

    elif filename == "urls.py":
        return "django_url"

    elif filename == "forms.py":
        return "django_form"

    elif filename.endswith(".html"):
        return "template"

    elif filename.endswith(".css"):
        return "css"

    elif filename.endswith(".js"):
        return "javascript"

    return "general"

# =========================================
# MAIN INDEXING
# =========================================

project_data = []
current_state = {}

print("\nScanning project...\n")

for root, dirs, files in os.walk(PROJECT_PATH):

    # Ignore folders
    dirs[:] = [

        d for d in dirs

        if d not in IGNORE_FOLDERS
    ]

    for file in files:

        # Ignore unwanted files
        if file in IGNORE_FILES:
            continue

        filepath = os.path.join(root, file)

        _, ext = os.path.splitext(file)

        # Skip unsupported files
        if ext not in ALLOWED_EXTENSIONS:
            continue

        try:

            file_hash = get_file_hash(filepath)

            current_state[filepath] = file_hash

            # Skip unchanged files
            if old_state.get(filepath) == file_hash:

                print(f"Skipping unchanged: {filepath}")

                continue

            print(f"Indexed changed/new file: {filepath}")

            stats = os.stat(filepath)

            content = read_file_content(filepath)

            chunks = create_chunks(content)

            # =========================================
            # BASE FILE INFO
            # =========================================

            file_info = {

                "file_name": file,

                "path": filepath,

                "module": detect_module(filepath),

                "file_type": detect_file_type(filepath),

                "extension": ext,

                "size_kb": round(stats.st_size / 1024, 2),

                "last_modified": datetime.fromtimestamp(
                    stats.st_mtime
                ).strftime("%Y-%m-%d %H:%M:%S"),

                "hash": file_hash,

                "total_chunks": len(chunks),

                "chunks": []
            }

            # =========================================
            # PYTHON METADATA
            # =========================================

            metadata = {}

            if ext == ".py":

                metadata = extract_python_metadata(content)

            # =========================================
            # STORE CHUNKS
            # =========================================

            for index, chunk in enumerate(chunks):

                chunk_data = {

                    "chunk_id": index,

                    "module": file_info["module"],

                    "file_type": file_info["file_type"],

                    "functions": metadata.get(
                        "functions",
                        []
                    ),

                    "classes": metadata.get(
                        "classes",
                        []
                    ),

                    "imports": metadata.get(
                        "imports",
                        []
                    ),

                    "models_used": metadata.get(
                        "models_used",
                        []
                    ),

                    "templates_used": metadata.get(
                        "templates_used",
                        []
                    ),

                    "content": chunk
                }

                file_info["chunks"].append(chunk_data)

            project_data.append(file_info)

        except Exception as e:

            print(f"\nError reading: {filepath}")

            print(e)

# =========================================
# SAVE INDEX
# =========================================

with open(INDEX_FILE, "w", encoding="utf-8") as f:

    json.dump(project_data, f, indent=4)

# =========================================
# SAVE STATE
# =========================================

with open(STATE_FILE, "w", encoding="utf-8") as f:

    json.dump(current_state, f, indent=4)

# =========================================
# FINISH
# =========================================

print("\nIndexing complete.")

print(f"Changed/New files indexed: {len(project_data)}")

print(f"Index saved to: {INDEX_FILE}")

print(f"State saved to: {STATE_FILE}")