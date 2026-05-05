import requests
import json
import os
import re
import time
from datetime import datetime
from hybrid_retriever import hybrid_search


OLLAMA_URL = "http://localhost:11434/api/generate"

MODELS = {
    "fast": "phi3:mini",
    "power": "llama3:latest"
}

LOG_FILE = "rag_log.json"


# ---------------- LOGGER ----------------

def log(action, data=None):
    entry = {
        "time": datetime.now().isoformat(),
        "action": action,
        "data": data
    }

    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)

    logs.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


# ---------------- CLASSIFIER ----------------

def classify(query):
    q = query.lower()

    if any(k in q for k in ["create module", "new module"]):
        return "module"

    if any(k in q for k in ["edit", "replace", "add", "modify"]):
        return "edit"

    return "analysis"


# ---------------- FILE HELPERS ----------------

def find_file(query):
    match = re.search(r'([\w/\\.-]+\.py)', query)

    if not match:
        return None

    name = os.path.basename(match.group(1))

    for root, _, files in os.walk("."):
        if name in files:
            return os.path.join(root, name)

    return None


def backup(file_path, lines):
    path = file_path + ".bak_" + datetime.now().strftime("%H%M%S")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    log("backup_created", path)


# ---------------- DIRECT ENGINE ----------------

def direct_replace(query, file_path):
    pattern = r'replace\s*-\s*(.*?)\s*-\s*to\s*-\s*(.*)'
    match = re.search(pattern, query, re.IGNORECASE)

    if not match:
        return False

    old = match.group(1)
    new = match.group(2)

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    backup(file_path, lines)

    for i, line in enumerate(lines):
        if old.strip().replace('"','') in line.replace('"',''):
            lines[i] = new + "\n"

            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            log("direct_replace", {"file": file_path, "old": old, "new": new})
            print("[UPDATED]")
            return True

    print("[TARGET NOT FOUND]")
    return False


# ---------------- MODULE CREATION ----------------

def create_module(name):
    base = f"./{name}"

    if os.path.exists(base):
        print("[EXISTS]")
        return

    os.makedirs(base, exist_ok=True)

    files = {
        "__init__.py": "",
        "models.py": "from django.db import models\n\n",
        "views.py": "from django.shortcuts import render\n\n",
        "urls.py": "from django.urls import path\n\nurlpatterns = []\n",
        "apps.py": f"""from django.apps import AppConfig

class {name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{name}'
"""
    }

    for fname, code in files.items():
        path = os.path.join(base, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        log("file_created", path)

    print("[MODULE CREATED]", name)


# ---------------- LLM ----------------

def call_llm(prompt):
    payload = {
        "model": MODELS["power"],
        "prompt": prompt,
        "stream": False
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=600)
        return res.json().get("response", "")
    except Exception as e:
        return str(e)


def extract_json(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                return None
    return None


# ---------------- LLM EDIT ----------------

def llm_edit(query, file_path):

    code = open(file_path, "r", encoding="utf-8").read()

    prompt = f"""
Modify this Python file.

FILE:
{file_path}

CODE:
{code}

Return ONLY JSON:

{{
  "operations": [
    {{
      "type": "replace_line",
      "target": "line",
      "code": "new line"
    }}
  ]
}}

Query:
{query}
"""

    res = call_llm(prompt)
    data = extract_json(res)

    if not data:
        print("[LLM FAILED]")
        return

    lines = open(file_path, "r").readlines()
    backup(file_path, lines)

    for op in data["operations"]:
        for i, line in enumerate(lines):
            if op["target"] in line:
                lines[i] = op["code"] + "\n"
                log("llm_edit", op)
                print("[LLM UPDATED]")
                break

    with open(file_path, "w") as f:
        f.writelines(lines)


# ---------------- ANALYSIS ----------------

def run_analysis(query):
    results = hybrid_search(query, top_k=4)

    context = "\n".join([r["chunk"]["code"][:600] for r in results])

    prompt = f"""
Answer based only on this context:

{context}

Query:
{query}
"""

    print(call_llm(prompt))


# ---------------- MAIN ----------------

def main():
    print("\nRAG AGENT \n")

    while True:
        query = input("\nQuery: ")

        if query.lower() == "exit":
            break

        mode = classify(query)

        print(f"\nMode: {mode}")

        if mode == "module":
            match = re.search(r'create module (\w+)', query.lower())
            if match:
                create_module(match.group(1))

        elif mode == "edit":
            file_path = find_file(query)

            if not file_path:
                print("[FILE NOT FOUND]")
                continue

            print("Target:", file_path)

            if not direct_replace(query, file_path):
                llm_edit(query, file_path)

        else:
            run_analysis(query)


if __name__ == "__main__":
    main()