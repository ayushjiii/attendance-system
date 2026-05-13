import os
import subprocess
import time


INDEXER_SCRIPT = "auto_indexer.py"

CACHE_FILE = "llm_cache.json"


def run_indexer():

    print(f"\nRUNNING: {INDEXER_SCRIPT}\n")

    start = time.time()

    result = subprocess.run(
        ["python", INDEXER_SCRIPT],
        text=True
    )

    end = time.time()

    elapsed = round(end - start, 2)

    if result.returncode == 0:

        print(f"\nINDEX UPDATED")

        print(f"TIME: {elapsed}s\n")

    else:

        print("\nINDEXER FAILED\n")


def clear_cache():

    if os.path.exists(CACHE_FILE):

        os.remove(CACHE_FILE)

        print("\nCACHE CLEARED\n")

    else:

        print("\nNO CACHE FILE FOUND\n")


def main():

    print("\nREFRESHING RAG\n")

    run_indexer()

    clear_cache()

    print("\nRAG READY\n")


if __name__ == "__main__":

    main()