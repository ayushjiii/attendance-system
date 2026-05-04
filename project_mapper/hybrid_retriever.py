from pathlib import Path
import json
import numpy as np
import re

from sentence_transformers import (
    SentenceTransformer
)


# FILES

INDEX_FILE = Path(
    "snapshots/hybrid/chunk_index.json"
)

EMBEDDINGS_FILE = Path(
    "snapshots/hybrid/chunk_embeddings.json"
)


# LOAD FILES

with open(
    INDEX_FILE,
    "r",
    encoding="utf-8"
) as f:

    indexed_chunks = json.load(f)


with open(
    EMBEDDINGS_FILE,
    "r",
    encoding="utf-8"
) as f:

    embedded_chunks = json.load(f)


# FAST LOOKUP

embedding_lookup = {}

for chunk in embedded_chunks:

    embedding_lookup[
        chunk["chunk_id"]
    ] = chunk["embedding"]


# LOAD EMBEDDING MODEL

print(
    "\nLOADING EMBEDDING MODEL...\n"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# NORMALIZATION

def normalize_text(text):

    return re.findall(
        r"\b\w+\b",
        text.lower()
    )


# LEXICAL SCORE

def lexical_score(

    query_words,

    search_words
):

    score = 0

    for word in query_words:

        if word in search_words:

            score += 1

    return score


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

    if denominator == 0:
        return 0

    return numerator / denominator


# GRAPH BOOST

def graph_boost(

    query_words,

    chunk
):

    boost = 0

    # RELATED MODELS

    for model_name in chunk[
        "related_models"
    ]:

        model_words = normalize_text(
            model_name
        )

        for word in model_words:

            if word in query_words:

                boost += 2

    # RELATED FUNCTIONS

    for function_name in chunk[
        "related_functions"
    ]:

        function_words = normalize_text(
            function_name
        )

        for word in function_words:

            if word in query_words:

                boost += 1

    return boost


# QUERY EXPANSION

def expand_query(query):

    replacements = {

        "workflow": "flow process steps",
        "architecture": "structure design modules",
        "reports": "report reporting analytics",
        "employees": "employee staff worker",
        "attendance": "attendance checkin checkout records",
        "leave": "leave vacation absence"
    }

    expanded = query.lower()

    for key, value in replacements.items():

        expanded = expanded.replace(
            key,
            value
        )

    return expanded


# HYBRID SEARCH

def hybrid_search(

    query,

    top_k=5
):

    expanded_query = expand_query(
        query
    )

    STOPWORDS = {

        "the",
        "is",
        "of",
        "a",
        "an",
        "how",
        "what",
        "can",
        "you",
        "does",
        "workflow",
        "explain",
        "tell",
        "about",
        "into",
        "from"
    }

    query_words = [

        word

        for word in normalize_text(
            expanded_query
        )

        if word not in STOPWORDS
    ]

    # QUERY EMBEDDING

    query_embedding = model.encode(
        expanded_query
    )

    results = []

    # SCORE EACH CHUNK

    for chunk in indexed_chunks:

        # LEXICAL

        search_words = normalize_text(

            chunk["search_text"]

        )

        lexical = lexical_score(

            query_words,

            search_words
        )

        # SEMANTIC

        chunk_embedding = embedding_lookup[
            chunk["chunk_id"]
        ]

        semantic = cosine_similarity(

            query_embedding,

            chunk_embedding
        )

        # GRAPH BOOST

        boost_score = graph_boost(

            query_words,

            chunk
        )

        file_path = chunk["file"].lower()

        # DOMAIN BOOSTING

        if "report" in query_words:

            if "reports" in file_path:

                boost_score += 3

        if "attendance" in query_words:

            if "attendance" in file_path:

                boost_score += 3

        if "leave" in query_words:

            if "leave" in file_path:

                boost_score += 3

        # IMPORTANT FUNCTION BOOST

        important_names = [

            "report",
            "attendance",
            "employee",
            "leave",
            "export",
            "summary"
        ]

        chunk_name = chunk["name"].lower()

        for word in important_names:

            if word in query_words and word in chunk_name:

                boost_score += 2

        # FINAL SCORE

        final_score = (

            lexical * 2.5

            +

            semantic

            +

            boost_score * 1.5
        )

        results.append({

            "final_score": final_score,

            "lexical": lexical,

            "semantic": semantic,

            "graph": boost_score,

            "chunk": chunk
        })

    # SORT

    results.sort(

        key=lambda x: x["final_score"],

        reverse=True
    )

    return results[:top_k]


# DISPLAY

def display_results(results):

    print("\n=================================")
    print("HYBRID RETRIEVAL RESULTS")
    print("=================================")

    for result in results:

        chunk = result["chunk"]

        print(f"\nNAME: {chunk['name']}")

        print(f"TYPE: {chunk['type']}")

        print(f"FILE: {chunk['file']}")

        print(
            f"\nFINAL SCORE: "
            f"{result['final_score']:.4f}"
        )

        print(
            f"LEXICAL: "
            f"{result['lexical']}"
        )

        print(
            f"SEMANTIC: "
            f"{result['semantic']:.4f}"
        )

        print(
            f"GRAPH BOOST: "
            f"{result['graph']}"
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

            for function_name in chunk[
                "related_functions"
            ]:

                print(f"- {function_name}")

        else:

            print("- None")

        print("\nCODE:\n")

        print(chunk["code"])

        print("\n" + "=" * 40)


# MENU

if __name__ == "__main__":

    print("\nHYBRID RETRIEVER\n")

    while True:

        query = input(

            "\nEnter query "
            "(or 'exit'): "

        )

        if query.lower() == "exit":

            break

        results = hybrid_search(
            query
        )

        display_results(results)