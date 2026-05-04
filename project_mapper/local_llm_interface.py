import requests
import time
import json
import hashlib
import os
from datetime import datetime
from hybrid_retriever import hybrid_search


OLLAMA_URL = "http://localhost:11434/api/generate"

MODELS = {
    "fast": "phi3:mini",
    "power": "llama3:latest"
}

TIMEOUT = 600
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


def get_cache_key(query, model, results):
    ids = [r["chunk"]["name"] for r in results]
    raw = f"{query}|{model}|{'-'.join(ids)}"
    return hashlib.md5(raw.encode()).hexdigest()


cache = load_cache()


# ---------------- QUERY ----------------

def classify_query(query):
    q = query.lower()

    if any(k in q for k in ["bug", "error", "fix", "issue", "debug"]):
        return "debug"

    if any(k in q for k in ["workflow", "flow", "architecture"]):
        return "deep"

    if any(k in q for k in ["add", "change", "modify", "update"]):
        return "edit"

    if any(k in q for k in ["what", "list", "show"]):
        return "simple"

    return "default"


def get_strategy(qtype):
    if qtype in ["debug", "deep", "edit"]:
        return {"model": MODELS["power"], "top_k": 4}
    return {"model": MODELS["fast"], "top_k": 3}


# ---------------- CONTEXT ----------------

def extract_logic(code):
    lines = code.split("\n")
    important = []

    for l in lines:
        l = l.strip()

        if any(k in l for k in [
            "def ", "class ", "return ",
            "filter(", "get(", "for ", "if ",
            "save(", "create("
        ]):
            important.append(l)

    return "\n".join(important[:30])


def build_context(results):
    parts = []

    for i, r in enumerate(results, 1):
        c = r["chunk"]
        logic = extract_logic(c["code"])

        parts.append(f"""
CHUNK {i}
NAME: {c['name']}
TYPE: {c['type']}
FILE: {c['file']}

LOGIC:
{logic}
""")

    return "\n".join(parts)


# ---------------- PROMPT ----------------

def build_prompt(query, context, edit_mode=False, fast_mode=False):

    if edit_mode:
        return f"""
You are modifying a Django codebase.

Return ONLY JSON:

{{
  "edits": [
    {{
      "file": "path/to/file.py",
      "operations": [
        {{
          "type": "insert_after",
          "target": "exact line",
          "code": "code"
        }},
        {{
          "type": "replace_line",
          "target": "exact line",
          "code": "new code"
        }},
        {{
          "type": "delete_line",
          "target": "line"
        }}
      ]
    }}
  ]
}}

Rules:
- Use exact lines from context
- Keep indentation correct
- No explanations

Query:
{query}

Context:
{context}
"""

    mode = "FAST MODE\n" if fast_mode else ""

    return f"""
{mode}

You are a code analysis assistant.

Rules:
- Use only context
- Be direct
- No assumptions

If incomplete:
Say: Context incomplete

Query:
{query}

Context:
{context}

Output:
1. Workflow
2. Data Flow
3. Key Functions
"""


# ---------------- LLM ----------------

def call_llm(model, prompt):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 200,
            "temperature": 0.2
        }
    }

    try:
        res = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=TIMEOUT
        )
        data = res.json()
        return data.get("response", "").strip()
    except Exception as e:
        return f"[ERROR] {e}"


# ---------------- EDIT ENGINE ----------------

def apply_edits(edit_json):
    if "edits" not in edit_json:
        print("[NO EDITS]")
        return

    for file_edit in edit_json["edits"]:
        file_path = file_edit["file"]

        if not os.path.exists(file_path):
            print(f"[SKIP] {file_path}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        backup = file_path + ".bak_" + datetime.now().strftime("%H%M%S")
        with open(backup, "w", encoding="utf-8") as f:
            f.writelines(lines)

        for op in file_edit["operations"]:
            op_type = op["type"]
            target = op.get("target", "")
            code = op.get("code", "")

            applied = False

            for i, line in enumerate(lines):
                if target.strip() in line.strip():

                    if op_type == "insert_after":
                        lines.insert(i + 1, code + "\n")

                    elif op_type == "replace_line":
                        lines[i] = code + "\n"

                    elif op_type == "delete_line":
                        lines.pop(i)

                    applied = True
                    break

            if not applied:
                print(f"[WARN] target not found: {target}")

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"[UPDATED] {file_path}")


def run_edit_flow(query, context, results):
    prompt = build_prompt(query, context, edit_mode=True)

    response = call_llm(MODELS["power"], prompt)

    if not response.strip():
        print("[EMPTY RESPONSE]")
        return

    try:
        edit_json = json.loads(response)
    except:
        print("[INVALID JSON]")
        print(response)
        return

    apply_edits(edit_json)


# ---------------- ANALYSIS ----------------

def smart_llm(query, context, results):

    fast_key = get_cache_key(query, MODELS["fast"], results)

    if fast_key in cache:
        print("\n[CACHE FAST]\n")
        fast_res = cache[fast_key]
    else:
        fast_prompt = build_prompt(query, context, fast_mode=True)
        fast_res = call_llm(MODELS["fast"], fast_prompt)
        cache[fast_key] = fast_res
        save_cache(cache)

    print(fast_res)

    if len(fast_res) > 80 and "incomplete" not in fast_res.lower():
        return

    print("\nRefining...\n")

    power_key = get_cache_key(query, MODELS["power"], results)

    if power_key in cache:
        print("\n[CACHE POWER]\n")
        power_res = cache[power_key]
    else:
        power_prompt = build_prompt(query, context)
        power_res = call_llm(MODELS["power"], power_prompt)
        cache[power_key] = power_res
        save_cache(cache)

    print(power_res)


# ---------------- UI ----------------

def display(results):
    print("\nRetrieved:")
    for r in results:
        c = r["chunk"]
        print(f"- {c['name']} ({c['type']})")


# ---------------- MAIN ----------------

def main():
    print("\nSMART LOCAL RAG (FINAL)\n")

    while True:
        query = input("\nQuery: ")

        if query.lower() == "exit":
            break

        t1 = time.time()

        qtype = classify_query(query)
        strategy = get_strategy(qtype)

        print(f"\nType: {qtype} | Model: {strategy['model']}")

        results = hybrid_search(query, top_k=strategy["top_k"])

        display(results)

        context = build_context(results)

        print("\nThinking...\n")

        if qtype == "edit":
            run_edit_flow(query, context, results)
        else:
            smart_llm(query, context, results)

        t2 = time.time()

        print(f"\nTime: {t2 - t1:.2f}s")


if __name__ == "__main__":
    main()