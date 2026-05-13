import json
import os
import difflib



# =========================
# CONFIG
# =========================

INDEX_FILE = "project_index.json"



# =========================
# LOAD INDEX
# =========================

def load_index():

    if not os.path.exists(INDEX_FILE):

        return []

    with open(
        INDEX_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



# =========================
# NORMALIZE
# =========================

def normalize(text):

    return (
        str(text)
        .lower()
        .replace("_", " ")
        .replace("-", " ")
        .strip()
    )



# =========================
# TOKENIZE
# =========================

def tokenize(text):

    return normalize(text).split()



# =========================
# FUZZY MATCH
# =========================

def fuzzy_match(word, target):

    similarity = difflib.SequenceMatcher(

        None,

        word,

        target

    ).ratio()

    return similarity



# =========================
# SCORE WORDS
# =========================

def score_word_match(
    query_words,
    target_text,
    exact_score,
    partial_score,
    fuzzy_score
):

    score = 0

    target_words = tokenize(target_text)

    for q_word in query_words:

        if len(q_word) <= 1:
            continue

        for t_word in target_words:

            # EXACT MATCH

            if q_word == t_word:

                score += exact_score

                continue


            # PARTIAL MATCH

            if (
                q_word in t_word
                or t_word in q_word
            ):

                score += partial_score

                continue


            # FUZZY MATCH

            similarity = fuzzy_match(
                q_word,
                t_word
            )

            if similarity >= 0.80:

                score += fuzzy_score

    return score



# =========================
# METADATA SCORE
# =========================

def calculate_metadata_score(
    query,
    chunk,
    file_name=""
):

    score = 0

    query_words = tokenize(query)


    # ------------------------
    # FILE NAME
    # ------------------------

    score += score_word_match(

        query_words,

        file_name,

        exact_score=25,

        partial_score=15,

        fuzzy_score=8
    )


    # ------------------------
    # MODULE
    # ------------------------

    module = chunk.get(
        "module",
        ""
    )

    score += score_word_match(

        query_words,

        module,

        exact_score=30,

        partial_score=20,

        fuzzy_score=10
    )


    # ------------------------
    # FILE TYPE
    # ------------------------

    file_type = chunk.get(
        "file_type",
        ""
    )

    score += score_word_match(

        query_words,

        file_type,

        exact_score=10,

        partial_score=5,

        fuzzy_score=3
    )


    # ------------------------
    # FUNCTIONS
    # ------------------------

    functions = chunk.get(
        "functions",
        []
    )

    for func in functions:

        score += score_word_match(

            query_words,

            func,

            exact_score=35,

            partial_score=20,

            fuzzy_score=10
        )


    # ------------------------
    # CLASSES
    # ------------------------

    classes = chunk.get(
        "classes",
        []
    )

    for cls in classes:

        score += score_word_match(

            query_words,

            cls,

            exact_score=35,

            partial_score=20,

            fuzzy_score=10
        )


    # ------------------------
    # IMPORTS
    # ------------------------

    imports = chunk.get(
        "imports",
        []
    )

    for imp in imports:

        score += score_word_match(

            query_words,

            imp,

            exact_score=10,

            partial_score=5,

            fuzzy_score=3
        )


    # ------------------------
    # MODELS USED
    # ------------------------

    models = chunk.get(
        "models_used",
        []
    )

    for model in models:

        score += score_word_match(

            query_words,

            model,

            exact_score=40,

            partial_score=25,

            fuzzy_score=12
        )


    # ------------------------
    # TEMPLATES USED
    # ------------------------

    templates = chunk.get(
        "templates_used",
        []
    )

    for template in templates:

        score += score_word_match(

            query_words,

            template,

            exact_score=15,

            partial_score=8,

            fuzzy_score=5
        )


    # ------------------------
    # CONTENT SCORE
    # ------------------------

    content = normalize(

        chunk.get(
            "content",
            ""
        )
    )

    for word in query_words:

        if len(word) <= 2:
            continue

        occurrences = content.count(word)

        score += min(
            occurrences,
            5
        )


    return score



# =========================
# SEARCH
# =========================

def metadata_search(
    query,
    top_k=10
):

    index = load_index()

    results = []


    for file_data in index:

        chunks = file_data.get(
            "chunks",
            []
        )

        for chunk in chunks:

            score = calculate_metadata_score(

                query,

                chunk,

                file_data.get(
                    "file_name",
                    ""
                )
            )

            if score <= 0:
                continue

            results.append({

                "score": score,

                "chunk": {

                    "file": file_data.get(
                        "path",
                        ""
                    ),

                    "name": file_data.get(
                        "file_name",
                        ""
                    ),

                    "module": chunk.get(
                        "module",
                        ""
                    ),

                    "functions": chunk.get(
                        "functions",
                        []
                    ),

                    "classes": chunk.get(
                        "classes",
                        []
                    ),

                    "models_used": chunk.get(
                        "models_used",
                        []
                    ),

                    "templates_used": chunk.get(
                        "templates_used",
                        []
                    ),

                    "code": chunk.get(
                        "content",
                        ""
                    )
                }
            })


    # ------------------------
    # SORT
    # ------------------------

    results = sorted(

        results,

        key=lambda x: x["score"],

        reverse=True
    )

    return results[:top_k]



# =========================
# TEST
# =========================

if __name__ == "__main__":

    while True:

        query = input("\nQuery: ")

        if query.lower() == "exit":
            break

        results = metadata_search(query)

        print("\nRESULTS:\n")

        if not results:

            print("No results found.")

            continue

        for r in results:

            print(
                f"[Score: {r['score']}] "
                f"{r['chunk']['name']}"
            )