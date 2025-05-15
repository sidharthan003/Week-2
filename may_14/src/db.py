# src/db.py

import os
import chromadb
from chromadb.config import Settings
from dataclasses import dataclass

PERSIST_DIR = "./db"

# Create the ChromaDB client with the new API
client = chromadb.PersistentClient(path=PERSIST_DIR)

@dataclass
class Chunk:
    text: str
    source: str
    page: int

def get_collection(name: str = "default"):
    return client.get_or_create_collection(name=name)

def index_chunks(ids: list, chunks: list, collection_name: str = "default"):
    col = get_collection(collection_name)
    
    # Convert chunks to proper format if they're not already Chunk objects
    if chunks and not isinstance(chunks[0], Chunk):
        # Assuming chunks are plain text strings here
        documents = chunks
        metadatas = [{"source": "unknown", "page": 0} for _ in chunks]
    else:
        documents = [c.text for c in chunks]
        metadatas = [{"source": c.source, "page": c.page} for c in chunks]

    col.add(documents=documents, metadatas=metadatas, ids=ids)

def retrieve(query: str, collection_name: str = "default", n_results: int = 3) -> list:
    col = get_collection(collection_name)
    results = col.query(query_texts=[query], n_results=n_results)
    return results["documents"][0] if results["documents"] else []