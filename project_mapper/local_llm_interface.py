import os
import re
import json
import hashlib
import requests
import time
from datetime import datetime

from hybrid_retriever import hybrid_search
from graph_retriever import graph_search


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "llama3:latest"

TIMEOUT = 600

CACHE_FILE = "llm_cache.json"


def load_cache():

    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return {}


def save_cache(cache):

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cache,
            f,
            indent=4
        )


def build_cache_key(query, retrieval_mode):

    raw = f"{query}|{retrieval_mode}"

    return hashlib.md5(
        raw.encode()
    ).hexdigest()


cache = load_cache()


def normalize(s):

    return (
        s.replace('"', '')
        .replace("'", "")
        .strip()
        .lower()
    )


def backup_file(file_path, lines):

    backup = (
        file_path
        + ".bak_"
        + datetime.now().strftime("%H%M%S")
    )

    with open(
        backup,
        "w",
        encoding="utf-8"
    ) as f:

        f.writelines(lines)

    print(f"[BACKUP] {backup}")


def log_edit(file_path, query):

    with open(
        "edit_log.txt",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"{datetime.now()} | "
            f"{file_path} | "
            f"{query}\n"
        )


def detect_file(query):

    match = re.search(
        r'([\w/\\.-]+\.py)',
        query
    )

    if not match:
        return None

    path = match.group(1)

    if os.path.exists(path):
        return path

    filename = os.path.basename(path)

    for root, _, files in os.walk("."):

        if filename in files:

            return os.path.join(
                root,
                filename
            )

    return None


def is_edit_request(query):

    q = query.lower()

    keywords = [

        "edit",
        "replace",
        "add after",
        "insert",
        "delete"

    ]

    return any(
        k in q
        for k in keywords
    )


def parse_intent(query):

    replace_match = re.search(

        r'replace\s*-\s*(.*?)\s*-\s*to\s*-\s*(.*)',

        query,

        re.I | re.S
    )

    if replace_match:

        return {

            "type": "replace",

            "old": replace_match.group(1).strip(),

            "new": replace_match.group(2).strip()
        }

    insert_match = re.search(

        r'add\s+after\s*(.*?)\s*->\s*(.*)',

        query,

        re.I | re.S
    )

    if insert_match:

        return {

            "type": "insert",

            "target": insert_match.group(1).strip(),

            "code": insert_match.group(2).strip()
        }

    return None


def apply_edit(file_path, intent, query):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        lines = f.readlines()

    original = lines[:]

    applied = False

    if intent["type"] == "replace":

        for i, line in enumerate(lines):

            if normalize(intent["old"]) == normalize(line):

                lines[i] = intent["new"] + "\n"

                applied = True

                break

    elif intent["type"] == "insert":

        for i, line in enumerate(lines):

            if normalize(intent["target"]) in normalize(line):

                indent = (
                    len(line)
                    - len(line.lstrip())
                )

                spaces = " " * indent

                lines.insert(

                    i + 1,

                    spaces
                    + intent["code"]
                    + "\n"
                )

                applied = True

                break

    if not applied:

        print("[ABORTED: target not found]")

        return

    backup_file(
        file_path,
        original
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.writelines(lines)

    log_edit(
        file_path,
        query
    )

    print("\n[EDIT APPLIED]\n")


def detect_retrieval_mode(query):

    q = query.lower()

    graph_keywords = [

        "dependency",
        "dependencies",
        "workflow",
        "flow",
        "impact",
        "connected",
        "relation",
        "relations",
        "trace",
        "architecture",
        "linked",
        "what uses",
        "depends on",
        "break if",
        "affected by"

    ]

    for keyword in graph_keywords:

        if keyword in q:

            return "graph"

    return "hybrid"


def detect_analysis_type(query):

    q = query.lower()

    if (
        "bug" in q
        or "issue" in q
        or "problem" in q
    ):

        return "bug"

    if (
        "workflow" in q
        or "flow" in q
        or "trace" in q
    ):

        return "workflow"

    if (
        "dependency" in q
        or "depends" in q
        or "connected" in q
        or "impact" in q
        or "break" in q
    ):

        return "dependency"

    return "general"


def build_prompt(query, context, analysis_type):

    return f"""
You are a senior Django codebase assistant.

Answer the query directly.

Rules:
- Be short and technical
- Do not write sections
- Do not explain obvious things
- Do not say "Based on the provided context"
- Do not say "The codebase appears to"
- Do not hallucinate
- If unsure, say "Not found in retrieved context"

QUERY:
{query}

CONTEXT:
{context}

Direct answer:
"""

def build_context(results):

    context = ""

    seen = set()

    for r in results:

        # GRAPH RETRIEVER FORMAT
        if "chunk" in r:

            chunk = r["chunk"]

            key = (
                chunk.get("file"),
                chunk.get("name")
            )

            if key in seen:
                continue

            seen.add(key)

            context += f"""

NAME: {chunk.get('name')}

TYPE: {chunk.get('type')}

FILE: {chunk.get('file')}

RELATED MODELS:
{", ".join(chunk.get("related_models", [])) or "None"}

RELATED FUNCTIONS:
{", ".join(chunk.get("related_functions", [])) or "None"}

CODE:
{chunk.get("code", "")[:1200]} 

-----------------------------------
"""

        # HYBRID / SEMANTIC FORMAT
        elif "text" in r:

            text = r.get("text", "")

            if text in seen:
                continue

            seen.add(text)

            context += f"""

CODE:
{text[:2000]}

-----------------------------------
"""

    return context


def call_llm(prompt):

    payload = {

        "model": MODEL,

        "prompt": prompt,

        "stream": False,

        "options": {

            "temperature": 0.2,

            "num_predict": 600
        }
    }

    try:

        res = requests.post(

            OLLAMA_URL,

            json=payload,

            timeout=TIMEOUT
        )

        return res.json().get(
            "response",
            ""
        )

    except Exception as e:

        return f"[ERROR] {e}"


def run_analysis(
    query,
    results,
    retrieval_mode,
    retrieval_time
):

    cache_key = build_cache_key(
        query,
        retrieval_mode
    )

    if cache_key in cache:

        print("\n[CACHE HIT]\n")

        print(cache[cache_key])

        return

    analysis_type = detect_analysis_type(query)

    context = build_context(results)

    prompt = build_prompt(
        query,
        context,
        analysis_type
    )

    llm_start = time.time()

    response = call_llm(prompt)

    llm_end = time.time()

    llm_time = round(
        llm_end - llm_start,
        2
    )

    total_time = round(
        retrieval_time + llm_time,
        2
    )

    print("\n=================================\n")

    if response.strip():

        print(response)

        cache[cache_key] = response

        save_cache(cache)

    else:

        print("[EMPTY RESPONSE]")

    print("\n=================================\n")

    print(f"Retrieval Mode: {retrieval_mode}")

    print(f"Retrieval Time: {retrieval_time}s")

    print(f"LLM Time: {llm_time}s")

    print(f"Total Time: {total_time}s")


def main():

    print("\nRAG ENGINE\n")

    while True:

        query = input("\nQuery: ")

        if query.lower() == "exit":
            break

        print("\nTHINKING...")

        if is_edit_request(query):

            file_path = detect_file(query)

            if not file_path:

                print("[FILE NOT FOUND]")

                continue

            intent = parse_intent(query)

            if not intent:

                print("[INVALID EDIT FORMAT]")

                continue

            print(f"\nTarget File: {file_path}")

            apply_edit(
                file_path,
                intent,
                query
            )

        else:

            retrieval_mode = detect_retrieval_mode(query)

            retrieval_start = time.time()

            if retrieval_mode == "graph":

                results = graph_search(query)

            else:

                results = hybrid_search(query)

            retrieval_end = time.time()

            retrieval_time = round(
                retrieval_end - retrieval_start,
                2
            )

            if not results:

                print("\n[NO RESULTS FOUND]\n")

                continue

            run_analysis(
                query,
                results,
                retrieval_mode,
                retrieval_time
            )


if __name__ == "__main__":

    main()