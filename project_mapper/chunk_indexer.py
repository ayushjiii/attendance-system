from pathlib import Path
import json


# FILES

CODE_CHUNKS_FILE = Path(
    "snapshots/raw/code_chunks.json"
)

MODEL_USAGE_FILE = Path(
    "snapshots/raw/model_usage.json"
)

CALL_GRAPH_FILE = Path(
    "snapshots/raw/detailed_call_graph.json"
)

OUTPUT_FILE = Path(
    "snapshots/hybrid/chunk_index.json"
)


# LOAD FILES

with open(
    CODE_CHUNKS_FILE,
    "r",
    encoding="utf-8"
) as f:

    code_chunks = json.load(f)


with open(
    MODEL_USAGE_FILE,
    "r",
    encoding="utf-8"
) as f:

    model_usage = json.load(f)


with open(
    CALL_GRAPH_FILE,
    "r",
    encoding="utf-8"
) as f:

    call_graph = json.load(f)


# INDEXED CHUNKS

indexed_chunks = []



# BUILD INDEX

for name, chunk_data in code_chunks.items():


    
    # RELATED MODELS
    

    related_models = model_usage.get(
        name,
        []
    )


    
    # RELATED FUNCTIONS
    

    related_functions = call_graph.get(
        name,
        []
    )


    
    # SEARCHABLE TEXT
    

    search_text = " ".join([

        name,

        chunk_data["type"],

        chunk_data["file"],

        " ".join(related_models),

        " ".join(related_functions),

        chunk_data["code"]

    ])


    
    # CHUNK ID
    

    chunk_id = (

        chunk_data["file"]
        .replace("\\", "_")
        .replace("/", "_")

        +

        "_"

        +

        name
    )


    
    # INDEX ENTRY
    

    indexed_chunk = {

        "chunk_id": chunk_id,

        "name": name,

        "type": chunk_data["type"],

        "file": chunk_data["file"],

        "start_line": chunk_data["start_line"],

        "end_line": chunk_data["end_line"],

        "related_models": related_models,

        "related_functions": related_functions,

        "code": chunk_data["code"],

        "search_text": search_text
    }


    indexed_chunks.append(
        indexed_chunk
    )



# SAVE INDEX
  

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        indexed_chunks,
        f,
        indent=4
    )


print(
    "\nCHUNK INDEX CREATED\n"
)