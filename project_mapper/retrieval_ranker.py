import os


# FILE FILTERS

IGNORED_FILES = {

    "old_model_mapper.py",
    "old_context_retriever.py",
    "old_impact_analyzer.py",

    "embedding_generator.py",
    "metadata_retriever.py",

    "chunk_indexer.py",
    "auto_indexer.py",

    "model_usage_mapper.py",
    "dependency_mapper.py",

    "function_mapper.py",
    "code_chunk_mapper.py",

    "hybrid_retriever.py",
    "graph_retriever.py",

    "retrieval_engine.py"
}



# QUERY INTENT


def detect_query_intent(query):

    query = query.lower()

    if any(word in query for word in [

        "workflow",
        "flow",
        "process",
        "steps",
        "pipeline",
        "execution",
        "request flow",
        "how works"

    ]):

        return "workflow"

    if any(word in query for word in [

        "model",
        "database",
        "schema",
        "table",
        "orm"

    ]):

        return "model"

    if any(word in query for word in [

        "dependency",
        "relation",
        "connected",
        "impact",
        "linked"

    ]):

        return "dependency"

    if any(word in query for word in [

        "bug",
        "issue",
        "problem",
        "error",
        "fix"

    ]):

        return "bug"

    return "general"



# TYPE BOOSTING


def apply_intent_boost(

    query,
    chunk
):

    intent = detect_query_intent(query)

    chunk_type = chunk.get(
        "type",
        ""
    ).lower()

    boost = 0


    # WORKFLOW


    if intent == "workflow":

        if chunk_type in [

            "django_view",
            "function",
            "django_url"

        ]:

            boost += 10

        if chunk_type in [

            "django_model",
            "general"

        ]:

            boost += 2


    # MODEL


    elif intent == "model":

        if chunk_type == "django_model":

            boost += 15

        if "model" in chunk.get(
            "name",
            ""
        ).lower():

            boost += 5


    # DEPENDENCY


    elif intent == "dependency":

        if chunk_type in [

            "function",
            "django_model",
            "django_view"

        ]:

            boost += 8


    # BUG


    elif intent == "bug":

        if chunk_type in [

            "function",
            "django_view"

        ]:

            boost += 10

    return boost



# FILE FILTER


def should_ignore_file(file_path):

    filename = os.path.basename(
        file_path
    )

    return filename in IGNORED_FILES



# DEDUPLICATION


def deduplicate_results(

    results,
    max_per_file=2
):

    final_results = []

    file_counter = {}

    seen_chunks = set()

    for result in results:

        chunk = result["chunk"]

        file_path = chunk["file"]

        chunk_id = chunk.get(
            "chunk_id",
            chunk["name"]
        )

        # SKIP DUPLICATE CHUNK

        if chunk_id in seen_chunks:

            continue

        seen_chunks.add(chunk_id)

        # FILE LIMIT

        current_count = file_counter.get(
            file_path,
            0
        )

        if current_count >= max_per_file:

            continue

        file_counter[file_path] = (

            current_count + 1
        )

        final_results.append(result)

    return final_results