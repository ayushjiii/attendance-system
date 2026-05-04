from pathlib import Path
import json

from sentence_transformers import (
    SentenceTransformer
)



# FILES


INDEX_FILE = Path(
    "snapshots/hybrid/chunk_index.json"
)

OUTPUT_FILE = Path(
    "snapshots/hybrid/chunk_embeddings.json"
)



# LOAD INDEX


with open(
    INDEX_FILE,
    "r",
    encoding="utf-8"
) as f:

    indexed_chunks = json.load(f)



# LOAD EMBEDDING MODEL


print(
    "\nLOADING EMBEDDING MODEL...\n"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



# GENERATE EMBEDDINGS

embedded_chunks = []


for chunk in indexed_chunks:


    print(
        f"Embedding: {chunk['name']}"
    )


    # TEXT TO EMBED

    text = chunk["search_text"]


    
    # GENERATE VECTOR
    

    embedding = model.encode(
        text
    ).tolist()


    # SAVE CHUNK

    embedded_chunk = {

        "chunk_id": chunk["chunk_id"],

        "name": chunk["name"],

        "type": chunk["type"],

        "file": chunk["file"],

        "related_models":
            chunk["related_models"],

        "related_functions":
            chunk["related_functions"],

        "code": chunk["code"],

        "embedding": embedding
    }


    embedded_chunks.append(
        embedded_chunk
    )


# SAVE EMBEDDINGS


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        embedded_chunks,
        f,
        indent=4
    )



# DONE


print(
    "\nCHUNK EMBEDDINGS CREATED\n"
)