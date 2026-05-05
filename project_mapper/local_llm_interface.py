import requests
import time
import json
import hashlib
import os
import re
from datetime import datetime
from hybrid_retriever import hybrid_search


OLLAMA_URL = "http://localhost:11434/api/generate"

MODELS = {
    "fast": "phi3:mini",
    "power": "llama3:latest"
}

TIMEOUT = 1000
CACHE_FILE = "llm_cache.json"


# ---------------- CACHE ----------------

def load_cache():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def get_cache_key(query, model):
    raw = f"{query}|{model}"
    return hashlib.md5(raw.encode()).hexdigest()

cache = load_cache()


# ---------------- UTILS ----------------

def normalize(s):
    return s.replace('"', '').replace("'", "").strip().lower()

def log_edit(file_path, query):
    with open("edit_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {file_path} | {query}\n")

def backup_file(file_path, content):
    backup = file_path + ".bak_" + datetime.now().strftime("%H%M%S")
    with open(backup, "w", encoding="utf-8") as f:
        f.writelines(content)
    print(f"[BACKUP CREATED] {backup}")


# ---------------- QUERY ----------------

def classify_query(query):
    q = query.lower()

    if any(k in q for k in ["bug", "error", "fix", "issue", "debug"]):
        return "debug"

    if any(k in q for k in ["workflow", "flow", "architecture"]):
        return "deep"

    if any(k in q for k in ["add", "change", "modify", "update", "edit", "replace", "create"]):
        return "edit"

    return "default"


# ---------------- FILE TARGETING ----------------

def detect_file_from_query(query):
    match = re.search(r'([\w/\\.-]+\.py)', query)
    if not match:
        return None

    requested = match.group(1)
    requested_name = os.path.basename(requested)

    if os.path.exists(requested):
        return requested

    for root, dirs, files in os.walk("."):
        for file in files:
            if file == requested_name:
                return os.path.join(root, file)

    return None


def select_target_file(query, results):
    q = query.lower()

    for r in results:
        path = r["chunk"]["file"].lower()
        if any(word in path for word in q.split()):
            return r["chunk"]["file"]

    return None


# ---------------- DIRECT EDIT ----------------

def try_direct_edit(query, file_path):

    pattern = r'replace\s*-\s*(.*?)\s*-\s*to\s*-\s*(.*)'
    match = re.search(pattern, query, re.IGNORECASE | re.DOTALL)

    if not match:
        print("[NO DIRECT PATTERN MATCH]")
        return False

    old = match.group(1).strip()
    new = match.group(2).strip()

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    original = lines[:]

    # -------- BLOCK REPLACE --------
    full_text = "".join(lines)

    if old in full_text:
        print("[BLOCK MATCH FOUND]")
        print("\n--- PREVIEW ---")
        print("OLD BLOCK:", old)
        print("NEW BLOCK:", new)

        full_text = full_text.replace(old, new)
        lines = full_text.splitlines(keepends=True)

        backup_file(file_path, original)

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print("[BLOCK EDIT APPLIED]")
        log_edit(file_path, query)
        return True

    # -------- LINE REPLACE --------
    for i, line in enumerate(lines):
        if normalize(old) in normalize(line):

            print("\n--- PREVIEW ---")
            print("OLD:", line.strip())
            print("NEW:", new)

            lines[i] = new + "\n"

            backup_file(file_path, original)

            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            print("[LINE EDIT APPLIED]")
            log_edit(file_path, query)
            return True

    print("[DIRECT EDIT FAILED]")
    return False


# ---------------- LLM ----------------

def call_llm(model, prompt):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 300,
            "temperature": 0.2
        }
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        return res.json().get("response", "").strip()
    except Exception as e:
        return f"[ERROR] {e}"


def build_edit_prompt(query, file_path, code):
    return f"""
Modify ONLY this file.

FILE:
{file_path}

CODE:
{code}

Return ONLY JSON:

{{
  "operations": [
    {{
      "type": "replace_line",
      "target": "exact line",
      "code": "new line"
    }},
    {{
      "type": "insert_after",
      "target": "exact line",
      "code": "new line"
    }}
  ]
}}

Rules:
- Use replace_line ONLY if replacing
- Use insert_after ONLY if adding
- Do not mix both unnecessarily
- No explanation
- Only JSON

Query:
{query}
"""

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


def apply_operations(file_path, edit_json):

    if not edit_json or "operations" not in edit_json:
        print("[INVALID JSON]")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    original = lines[:]

    for op in edit_json["operations"]:
        op_type = op["type"]
        target = op["target"]
        code = op["code"]

        for i, line in enumerate(lines):

            if target.strip() in line.strip():

                print("[LLM EDIT MATCH FOUND]")

                if op_type == "replace_line":
                    lines[i] = code + "\n"

                elif op_type == "insert_after":
                    lines.insert(i + 1, code + "\n")

                break

    backup_file(file_path, original)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print("[LLM EDIT APPLIED]")


# ---------------- EDIT FLOW ----------------

def run_edit_flow(query, results):

    target_file = detect_file_from_query(query)

    if not target_file:
        target_file = select_target_file(query, results)

    if not target_file:
        print("[NO FILE FOUND]")
        return

    print(f"\nTarget File: {target_file}")

    # STEP 1 — DIRECT EDIT
    
    success = try_direct_edit(query, target_file)

    if success:
        return

    # 🚫 STOP unsafe fallback for replace queries
    if "replace" in query.lower():
        print("[ABORTED: TARGET NOT FOUND]")
        return

    # STEP 2 — LLM FALLBACK (only safe ops like add)
    print("[USING LLM FALLBACK]")

    code = open(target_file, "r", encoding="utf-8").read()
    prompt = build_edit_prompt(query, target_file, code)

    response = call_llm(MODELS["power"], prompt)
    edit_json = extract_json(response)

    if edit_json:
        apply_operations(target_file, edit_json)
    else:
        print("[FAILED: LLM COULD NOT FIX]")


# ---------------- MAIN ----------------

def main():
    print("\nRAG MODE ~~~ \n")

    while True:
        print("------------------------")
        query = input("\nQuery: ")
        print("------------------------")
        if query.lower() == "exit":
            break

        qtype = classify_query(query)

        results = hybrid_search(query, top_k=4)

        print("\nRetrieved:")
        for r in results:
            print("-", r["chunk"]["name"])

        print("\nThinking...\n")

        if qtype == "edit":
            run_edit_flow(query, results)
        else:
            print("Analysis mode not implemented.")


if __name__ == "__main__":
    main()