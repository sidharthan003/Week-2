import chromadb
from chromadb.config import Settings

# Initialize Chroma
client = chromadb.Client(Settings(anonymized_telemetry=False))
collection = client.create_collection(name="sample_collection")

# Sample Document
sample_text = "This is a test document for ChromaDB."

# Add to collection
collection.add(documents=[sample_text], ids=["doc1"])

# Confirm insertion
results = collection.get(ids=["doc1"])
print("Stored Document:", results["documents"][0])
