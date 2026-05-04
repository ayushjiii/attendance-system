import requests
import time
import json
import hashlib
from hybrid_retriever import hybrid_search


OLLAMA_URL = "http://localhost:11434/api/generate"

MODELS = {
    "fast": "phi3:mini",
    "power": "llama3:latest"
}

TIMEOUT = 600
CACHE_FILE = "llm_cache.json"


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

    return "\n".join(important[:25])


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


def build_prompt(query, context, fast_mode=False):
    mode = "FAST MODE\n" if fast_mode else ""

    return f"""
You are a code analysis assistant.

{mode}

Rules:
- Use only the given context
- No assumptions
- No questions
- Be direct

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

Keep it concise.
"""


def call_llm(model, prompt):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 200,
            "temperature": 0.2,
            "top_k": 20,
            "top_p": 0.7,
            "repeat_penalty": 1.1
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


def smart_llm(query, context, results):
    fast_key = get_cache_key(query, MODELS["fast"], results)

    if fast_key in cache:
        print("\n[CACHE - FAST]\n")
        fast_res = cache[fast_key]
    else:
        fast_prompt = build_prompt(query, context, fast_mode=True)
        fast_res = call_llm(MODELS["fast"], fast_prompt)
        cache[fast_key] = fast_res
        save_cache(cache)

    print(fast_res)

    if len(fast_res) > 80 and "incomplete" not in fast_res.lower():
        return fast_res

    print("\nRefining...\n")

    power_key = get_cache_key(query, MODELS["power"], results)

    if power_key in cache:
        print("\n[CACHE - POWER]\n")
        power_res = cache[power_key]
    else:
        power_prompt = build_prompt(query, context)
        power_res = call_llm(MODELS["power"], power_prompt)
        cache[power_key] = power_res
        save_cache(cache)

    print(power_res)

    return power_res


def display(results):
    print("\nRetrieved:")
    for r in results:
        c = r["chunk"]
        print(f"- {c['name']} ({c['type']})")


def main():
    print("\nSMART LOCAL RAG\n")

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

        smart_llm(query, context, results)

        t2 = time.time()

        print(f"\nTime: {t2 - t1:.2f}s")


if __name__ == "__main__":
    main()