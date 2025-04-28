import os
import requests
import time
from chromadb import HttpClient
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

# Get API key for Euri
EURI_API_KEY = os.getenv("EURI_API_KEY")

# Connect to the running ChromaDB server
client = HttpClient(host="localhost", port=8000)
print("Connected to ChromaDB server")

# Get or create collection
collection = client.get_or_create_collection("my_test_collection")
print(f"Collection: {collection.name}")

# Function to generate embeddings using Euri API
def generate_embeddings(text_list):
    url = "https://api.euron.one/api/v1/euri/alpha/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {EURI_API_KEY}"
    }
    payload = {
        "input": text_list,
        "model": "text-embedding-3-small"
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    # Extract embeddings
    embeddings = [item['embedding'] for item in data["data"]]
    return embeddings

# Sample documents (properly separated)
documents = [
    "The patient has a confirmed diagnosis of Opioid Use Disorder based on DSM-5 criteria.",
    "She reports a history of escalating opioid use following a back injury three years ago.",
    "Despite multiple attempts to reduce usage, the patient continues to experience cravings and withdrawal symptoms.",
    "He has previously engaged in outpatient MAT but relapsed after six months.",
    "The patient expresses a strong interest in reinitiating buprenorphine treatment and engaging with behavioral therapy.",
    "Urine drug screen is positive for fentanyl and negative for prescribed buprenorphine.",
    "Social support is limited, and the patient reports housing instability as a barrier to treatment adherence.",
    "She denies current injection drug use but has a history of heroin use by injection.",
    "The care team recommends initiating a harm reduction approach alongside MOUD.",
    "Follow-up is scheduled in one week to monitor withdrawal symptoms and assess treatment engagement."
]

# Generate embeddings
print("Generating embeddings...")
all_embeddings = generate_embeddings(documents)
print(f"Generated {len(all_embeddings)} embeddings")
print(f"Embedding dimension: {len(all_embeddings[0])}")

# Add documents to the collection with error handling
print("Adding documents to ChromaDB...")
for idx, (doc, emb) in enumerate(zip(documents, all_embeddings)):
    try:
        collection.add(
            documents=[doc],
            embeddings=[emb],
            metadatas=[{"source": "my_test_collection"}],
            ids=[f"doc_{idx}"]
        )
        print(f"Added document {idx}")
        time.sleep(0.5)  # Small delay between requests to avoid overloading the server
    except Exception as e:
        print(f"Error adding document {idx}: {e}")

# Try to retrieve the documents with error handling
print("Retrieving documents from ChromaDB...")
try:
    results = collection.get(include=["documents", "embeddings"])
    print(f"Retrieved {len(results['ids'])} documents")
except Exception as e:
    print(f"Error retrieving documents: {e}")

print(collection.get(include=["documents", "embeddings"]))