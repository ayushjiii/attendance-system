import requests
import time
import json
import hashlib
from hybrid_retriever import hybrid_search



# CONFIG


OLLAMA_URL = "http://localhost:11434/api/generate"

MODELS = {
    "fast": "phi3:mini",
    "power": "llama3:latest"
}

TIMEOUT = 600 ##  timeout in seconds
CACHE_FILE = "llm_cache.json"



# CACHE


def load_cache():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def get_cache_key(query, model, strategy):
    raw = f"{query}|{model}|{strategy['top_k']}|{strategy['max_chars']}"
    return hashlib.md5(raw.encode()).hexdigest()

cache = load_cache()



# QUERY CLASSIFIER


def classify_query(query: str):
    q = query.lower()

    if any(k in q for k in ["bug", "error", "fix", "issue", "debug"]):
        return "debug"

    if any(k in q for k in ["add", "change", "modify", "update"]):
        return "edit"

    if any(k in q for k in ["workflow", "flow", "architecture", "data flow"]):
        return "deep"

    if any(k in q for k in ["what", "list", "show"]):
        return "simple"

    return "default"


# STRATEGY (use model based on need)


def get_strategy(query_type):

    if query_type == "edit":
        return {"model": MODELS["power"], "top_k": 3, "max_chars": 2000}

    if query_type == "debug":
        return {"model": MODELS["power"], "top_k": 4, "max_chars": 3000}

    if query_type == "deep":
        return {"model": MODELS["power"], "top_k": 3, "max_chars": 2000}

    if query_type == "simple":
        return {"model": MODELS["fast"], "top_k": 2, "max_chars": 800}

    return {"model": MODELS["fast"], "top_k": 3, "max_chars": 1000}



# FAST MODE (NO LLM)


def fast_mode(query, results):
    q = query.lower()

    if "list" in q or "show" in q:
        print("\n FAST MODE (no LLM)\n")
        for r in results:
            c = r["chunk"]
            print(f"- {c['name']} ({c['type']}) → {c['file']}")
        return True

    return False


# CONTEXT


def build_context(results, strategy):
    parts = []

    for i, r in enumerate(results, 1):
        c = r["chunk"]

        parts.append(f"""
FUNCTION START
Name: {c['name']}
File: {c['file']}

{c['code'][:strategy['max_chars']]}
FUNCTION END
""")

    return "\n".join(parts)



# PROMPT


def build_prompt(query, context, mode, model):

    # SIMPLE → relaxed prompt for phi3
    if model == MODELS["fast"]:
        return f"""
Explain briefly.

Query:
{query}

Code:
{context}
"""

    # EDIT MODE (prompt for editing code)
    if mode == "edit":
        return f"""
You are a code editing assistant.

Rules:
- Only use given code
- No assumptions

Query:
{query}

Code:
{context}
"""

    # DEFAULT / DEEP
    return f"""
Explain clearly.

Query:
{query}

Code:
{context}

keep the output minimal and accurate dont be oversmart or overwrite anything.

"""



# LLM CALL 

def ask_llm(model, prompt, query):

    key = get_cache_key(query, model)

    
    # CACHE HIT
    
    if key in cache:
        print("\n CACHE HIT\n")
        print(cache[key])
        return cache[key]

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_predict": 200,
            "temperature": 0.2
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True,
            timeout=TIMEOUT
        )

        full = ""

        
        # STREAM MODE

        for line in response.iter_lines():
            if not line:
                continue

            try:
                data = json.loads(line.decode("utf-8"))

                token = data.get("response", "")
                if token:
                    print(token, end="", flush=True)
                    full += token

                if data.get("done", False):
                    break

            except:
                continue

        
        # IF EMPTY → RETRY (NON-STREAM)
        
        if not full.strip():
            print("\n EMPTY → retrying without stream...\n")

            payload["stream"] = False

            retry = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=TIMEOUT
            )

            data = retry.json()
            full = data.get("response", "")

            if full:
                print(full)
            else:
                print("\n[FAILED] Model returned empty response.")
                return "[EMPTY RESPONSE]"

        
        # SAVE CACHE (ONLY VALID)
        
        if full.strip():
            cache[key] = full
            save_cache(cache)

        return full

    except Exception as e:
        return f"\n[ERROR] {e}"


# DISPLAY


def display(results):
    print("\n--- RETRIEVED ---")
    for r in results:
        c = r["chunk"]
        print(f"{c['name']} ({c['type']})")



# MAIN


def main():
    print("\nSMART LOCAL RAG (STABLE)\n")

    while True:
        query = input("\nQuery: ").strip()

        #  prevent empty query
        if not query:
            print(" Empty query. Try again.")
            continue

        if query.lower() == "exit":
            break

        qtype = classify_query(query)
        strategy = get_strategy(qtype)

        print(f"\nType: {qtype} | Model: {strategy['model']}")

        t1 = time.time()
        results = hybrid_search(query, top_k=strategy["top_k"])
        t2 = time.time()

        print(f" Retrieval: {t2 - t1:.2f}s")
        display(results)

        # fast mode
        if fast_mode(query, results):
            continue

        context = build_context(results, strategy)
        prompt = build_prompt(query, context, qtype, strategy["model"])

        print("\nTHINKING...\n")

        ask_llm(strategy["model"], prompt, query, strategy)

        t3 = time.time()

        print(f"\n Total: {t3 - t1:.2f}s")

if __name__ == "__main__":
    main()