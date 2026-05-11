import os
import re
import json
import hashlib
import requests
import time
from datetime import datetime

from hybrid_retriever import hybrid_search
from graph_retriever import graph_search


# =========================================================
# CONFIG
# =========================================================

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "llama3:latest"

TIMEOUT = 600

CACHE_FILE = "llm_cache.json"


# =========================================================
# CACHE
# =========================================================

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


# =========================================================
# UTIL
# =========================================================

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


# =========================================================
# FILE DETECTION
# =========================================================

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


# =========================================================
# EDIT REQUEST DETECTION
# =========================================================

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


# =========================================================
# PARSE EDIT INTENT
# =========================================================

def parse_intent(query):

    # ---------------- REPLACE ----------------

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

    # ---------------- INSERT ----------------

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


# =========================================================
# APPLY EDIT
# =========================================================

def apply_edit(file_path, intent, query):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        lines = f.readlines()

    original = lines[:]

    applied = False

    # =====================================================
    # REPLACE
    # =====================================================

    if intent["type"] == "replace":

        for i, line in enumerate(lines):

            if normalize(intent["old"]) == normalize(line):

                print("\n[MATCH FOUND]\n")

                print("OLD:", line.strip())

                print("NEW:", intent["new"])

                lines[i] = intent["new"] + "\n"

                applied = True

                break

    # =====================================================
    # INSERT
    # =====================================================

    elif intent["type"] == "insert":

        for i, line in enumerate(lines):

            if normalize(intent["target"]) in normalize(line):

                print("\n[INSERT AFTER]\n")

                print("TARGET:", line.strip())

                print("INSERT:", intent["code"])

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

    # =====================================================
    # FAIL
    # =====================================================

    if not applied:

        print("[ABORTED: target not found]")

        return

    # =====================================================
    # SAVE
    # =====================================================

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


# =========================================================
# RETRIEVAL MODE
# =========================================================

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


# =========================================================
# ANALYSIS TYPE
# =========================================================

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
    ):

        return "dependency"

    return "general"


# =========================================================
# PROMPTS
# =========================================================

def build_bug_prompt(query, context):

    return f"""
Find possible bugs using ONLY the context.

QUERY:
{query}

CONTEXT:
{context}
"""


def build_workflow_prompt(query, context):

    return f"""
Explain workflow using ONLY the context.

QUERY:
{query}

CONTEXT:
{context}
"""


def build_dependency_prompt(query, context):

    return f"""
Analyze dependencies using ONLY the context.

QUERY:
{query}

CONTEXT:
{context}
"""


def build_general_prompt(query, context):

    return f"""
Answer using ONLY the provided context.

QUERY:
{query}

CONTEXT:
{context}
"""


# =========================================================
# PROMPT ROUTER
# =========================================================

def build_prompt(query, context):

    analysis_type = detect_analysis_type(query)

    if analysis_type == "bug":

        return build_bug_prompt(
            query,
            context
        )

    if analysis_type == "workflow":

        return build_workflow_prompt(
            query,
            context
        )

    if analysis_type == "dependency":

        return build_dependency_prompt(
            query,
            context
        )

    return build_general_prompt(
        query,
        context
    )


# =========================================================
# LLM
# =========================================================

def call_llm(prompt):

    payload = {

        "model": MODEL,

        "prompt": prompt,

        "stream": False,

        "options": {

            "temperature": 0.2,

            "num_predict": 1000
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


# =========================================================
# ANALYSIS
# =========================================================

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

    # =====================================================
    # CACHE HIT
    # =====================================================

    if cache_key in cache:

        print("\n[CACHE HIT]\n")

        print(cache[cache_key])

        print("\n------------------------")

        print(
            "Retrieval Time: 0.0s"
        )

        print(
            "LLM Time: 0.0s"
        )

        print(
            "Total Time: CACHE"
        )

        print("------------------------")

        return

    # =====================================================
    # BUILD CONTEXT
    # =====================================================

    context = ""

    for r in results:

        chunk = r["chunk"]

        context += f"""

FILE: {chunk['file']}

NAME: {chunk['name']}

{chunk['code'][:1200]}

-------------------
"""

    # =====================================================
    # PROMPT
    # =====================================================

    prompt = build_prompt(
        query,
        context
    )

    # =====================================================
    # LLM
    # =====================================================

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

    print(f"LLM Time: {llm_time}s")

    total_time = retrieval_time + llm_time

    print(f"Total Time: {total_time}s")


    if response.strip():

        print(response)

        print("\n------------------------")

        print(
            f"Retrieval Time: "
            f"{retrieval_time}s"
        )

        print(
            f"LLM Time: "
            f"{llm_time}s"
        )

        print(
            f"Total Time: "
            f"{total_time}s"
        )

        print(
            f"Retrieval Mode: "
            f"{retrieval_mode}"
        )

        print("------------------------")

        cache[cache_key] = response

        save_cache(cache)

    else:

        print("[EMPTY RESPONSE]")


# =========================================================
# MAIN
# =========================================================

def main():

    print("\nRAG ENGINE V2 (STABLE)\n")

    while True:

        query = input("\nQuery: ")

        if query.lower() == "exit":
            break

        # =================================================
        # EDIT MODE
        # =================================================

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

        # =================================================
        # ANALYSIS MODE
        # =================================================

        else:

            retrieval_mode = detect_retrieval_mode(query)

            print(
                f"\nRetrieval Mode: "
                f"{retrieval_mode}"
            )

            # ---------------------------------------------

            retrieval_start = time.time()

            if retrieval_mode == "graph":

                results = graph_search(query)

            else:

                results = hybrid_search(
                    query,
                    top_k=4
                )

            retrieval_end = time.time()

            retrieval_time = round(
                retrieval_end - retrieval_start,
                2
            )

            print(f"Retrieval Time: {retrieval_time}s")

            print("\nRetrieved:")

            for r in results:

                print(
                    "-",
                    r["chunk"]["name"]
                )

            print("\nThinking...\n")

            run_analysis(
                query,
                results,
                retrieval_mode,
                retrieval_time
            )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    main()