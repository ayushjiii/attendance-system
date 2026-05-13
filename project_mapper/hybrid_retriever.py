import json
from pathlib import Path

from graph_retriever import graph_search
from sementic_retriever import semantic_search


GRAPH_WEIGHT = 2
SEMANTIC_WEIGHT = 3


def normalize_results(results, source_type):

    normalized = []

    for r in results:

        chunk = r.get("chunk", "")

        if isinstance(chunk, dict):

            text = chunk.get("code", "")

        else:

            text = str(chunk)

        normalized.append({

            "text": text,
            "score": r.get("score", 1),
            "source": source_type
        })

    return normalized


def merge_results(graph_results, semantic_results):

    merged = {}

    # graph results

    for r in graph_results:

        text = r["text"]

        score = r["score"] * GRAPH_WEIGHT

        if text not in merged:

            merged[text] = r

            merged[text]["score"] = score

        else:

            merged[text]["score"] += score

    # semantic results

    for r in semantic_results:

        text = r["text"]

        score = r["score"] * SEMANTIC_WEIGHT

        if text not in merged:

            merged[text] = r

            merged[text]["score"] = score

        else:

            merged[text]["score"] += score

    final = list(merged.values())

    final.sort(

        key=lambda x: x["score"],
        reverse=True
    )

    return final


def hybrid_search(query):

    graph_results = graph_search(query)

    semantic_results = semantic_search(query)

    graph_results = normalize_results(

        graph_results,
        "graph"
    )

    semantic_results = normalize_results(

        semantic_results,
        "semantic"
    )

    final = merge_results(

        graph_results,
        semantic_results
    )

    return final[:15]


if __name__ == "__main__":

    while True:

        q = input("\nQuery: ")

        if q == "exit":

            break

        results = hybrid_search(q)

        print("\nRESULTS\n")

        for r in results:

            print("=" * 50)

            print("SOURCE:", r["source"])

            print("SCORE:", r["score"])

            print()

            print(r["text"])