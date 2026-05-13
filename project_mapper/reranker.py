# =========================
# REMOVE DUPLICATES
# =========================

def remove_duplicate_results(results):

    unique = []

    seen = set()

    for result in results:

        chunk = result["chunk"]

        file_name = chunk.get(
            "name",
            ""
        )

        chunk_code = chunk.get(
            "code",
            ""
        )

        unique_key = (
            file_name
            + str(len(chunk_code))
        )

        if unique_key in seen:
            continue

        seen.add(unique_key)

        unique.append(result)

    return unique



# =========================
# BOOST IMPORTANT FILES
# =========================

def boost_important_results(
    query,
    results
):

    query = query.lower()

    for result in results:

        chunk = result["chunk"]

        file_name = chunk.get(
            "name",
            ""
        ).lower()

        module = chunk.get(
            "module",
            ""
        ).lower()

        functions = chunk.get(
            "functions",
            []
        )

        classes = chunk.get(
            "classes",
            []
        )


        # ------------------------
        # FILE NAME BOOST
        # ------------------------

        if any(
            word in file_name
            for word in query.split()
        ):

            result["score"] += 20


        # ------------------------
        # MODULE BOOST
        # ------------------------

        if any(
            word == module
            for word in query.split()
        ):

            result["score"] += 30


        # ------------------------
        # FUNCTION BOOST
        # ------------------------

        for func in functions:

            if func.lower() in query:

                result["score"] += 25


        # ------------------------
        # CLASS BOOST
        # ------------------------

        for cls in classes:

            if cls.lower() in query:

                result["score"] += 25


    return results



# =========================
# LIMIT SAME FILE SPAM
# =========================

def diversify_results(
    results,
    max_per_file=2
):

    final_results = []

    file_counter = {}

    for result in results:

        file_name = result["chunk"].get(
            "name",
            ""
        )

        current_count = file_counter.get(
            file_name,
            0
        )

        if current_count >= max_per_file:
            continue

        final_results.append(result)

        file_counter[file_name] = (
            current_count + 1
        )

    return final_results



# =========================
# MAIN RERANKER
# =========================

def rerank_results(
    query,
    results,
    top_k=10
):

    # REMOVE DUPLICATES

    results = remove_duplicate_results(
        results
    )


    # BOOST IMPORTANT

    results = boost_important_results(

        query,

        results
    )


    # SORT AGAIN

    results = sorted(

        results,

        key=lambda x: x["score"],

        reverse=True
    )


    # DIVERSIFY FILES

    results = diversify_results(
        results
    )


    return results[:top_k]