from pathlib import Path
import json



# INDEX FILE


INDEX_FILE = Path(
    "snapshots/hybrid/chunk_index.json"
)



# LOAD INDEX

with open(
    INDEX_FILE,
    "r",
    encoding="utf-8"
) as f:

    indexed_chunks = json.load(f)



# TEXT NORMALIZATION


def normalize_text(text):


    return text.lower().split()



# SCORING FUNCTION


def calculate_score(


    query_words,

    search_words
):


    score = 0


    for word in query_words:


        if word in search_words:

            score += 1


    return score


# SEARCH ENGINE

def search_chunks(


    query,

    top_k=5
):


    query_words = normalize_text(
        query
    )


    results = []


    # SEARCH ALL CHUNKS
    

    for chunk in indexed_chunks:


        search_words = normalize_text(

            chunk["search_text"]

        )


        score = calculate_score(

            query_words,

            search_words
        )


        
        # IGNORE ZERO MATCHES
        

        if score > 0:


            results.append({

                "score": score,

                "chunk": chunk
            })


    
    # SORT BY SCORE
    

    results.sort(

        key=lambda x: x["score"],

        reverse=True
    )


    return results[:top_k]



# DISPLAY RESULTS


def display_results(results):


    if not results:

        print("\nNo results found\n")

        return


    print("\n=================================")
    print("RETRIEVAL RESULTS")
    print("=================================")


    for result in results:


        score = result["score"]

        chunk = result["chunk"]


        print(f"\nNAME: {chunk['name']}")

        print(f"TYPE: {chunk['type']}")

        print(f"FILE: {chunk['file']}")

        print(f"SCORE: {score}")


        print("\nRELATED MODELS:")

        if chunk["related_models"]:

            for model in chunk["related_models"]:

                print(f"- {model}")

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


print("\nRETRIEVAL ENGINE\n")


while True:


    query = input(

        "\nEnter query "
        "(or 'exit'): "

    )


    if query.lower() == "exit":

        break


    results = search_chunks(
        query
    )


    display_results(results)