from pathlib import Path
import json
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)


# FILE

EMBEDDINGS_FILE = Path(
    "snapshots/hybrid/chunk_embeddings.json"
)


# LOAD EMBEDDINGS

with open(
    EMBEDDINGS_FILE,
    "r",
    encoding="utf-8"
) as f:

    embedded_chunks = json.load(f)


# LOAD MODEL

print(
    "\nLOADING EMBEDDING MODEL...\n"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



# COSINE SIMILARITY


def cosine_similarity(


    vector_a,

    vector_b
):


    vector_a = np.array(vector_a)

    vector_b = np.array(vector_b)


    numerator = np.dot(
        vector_a,
        vector_b
    )


    denominator = (

        np.linalg.norm(vector_a)

        *

        np.linalg.norm(vector_b)

    )


    return numerator / denominator



# SEMANTIC SEARCH


def semantic_search(


    query,

    top_k=5
):

    # EMBED QUERY

    query_embedding = model.encode(
        query
    )


    results = []



    # COMPARE AGAINST CHUNKS


    for chunk in embedded_chunks:


        similarity = cosine_similarity(

            query_embedding,

            chunk["embedding"]
        )


        results.append({

            "similarity": similarity,

            "chunk": chunk
        })


    # SORT RESULTS

    results.sort(

        key=lambda x: x["similarity"],

        reverse=True
    )


    return results[:top_k]



# DISPLAY


def display_results(results):


    print("\n=================================")
    print("SEMANTIC RETRIEVAL RESULTS")
    print("=================================")


    for result in results:


        similarity = result["similarity"]

        chunk = result["chunk"]


        print(f"\nNAME: {chunk['name']}")

        print(f"TYPE: {chunk['type']}")

        print(f"FILE: {chunk['file']}")

        print(
            f"SIMILARITY: "
            f"{similarity:.4f}"
        )


        print("\nRELATED MODELS:")


        if chunk["related_models"]:

            for model_name in chunk[
                "related_models"
            ]:

                print(f"- {model_name}")

        else:

            print("- None")


        print("\nRELATED FUNCTIONS:")


        if chunk["related_functions"]:

            for function in chunk[
                "related_functions"
            ]:

                print(f"- {function}")

        else:

            print("- None")


        print("\nCODE:\n")

        print(chunk["code"])

        print("\n" + "=" * 40)


# MENU


print("\nSEMANTIC RETRIEVER\n")


while True:


    query = input(

        "\nEnter semantic query "
        "(or 'exit'): "

    )


    if query.lower() == "exit":

        break


    results = semantic_search(
        query
    )


    display_results(results)