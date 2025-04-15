import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv
load_dotenv()
import os



# === Load Assets ===
print("\n🔌 Loading index and metadata...")
index = faiss.read_index("./Data/rag_chunks/financial_index.faiss")
with open("./Data/rag_chunks/texts.pkl", "rb") as f:
    texts = pickle.load(f)
with open("./Data/rag_chunks/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

# === Load Embedding Model ===
model = SentenceTransformer("all-MiniLM-L6-v2")

# === Together AI Config ===
import os
import requests
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")  # Set this in your environment
TOGETHER_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

headers = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

def embed_query(query):
    return model.encode([query])[0].astype(np.float32)

def search_index(query, top_k=5):
    query_vector = embed_query(query)
    D, I = index.search(np.array([query_vector]), top_k)
    return [(texts[i], metadata[i]) for i in I[0]]

def build_prompt(context_chunks, query):
    context = "\n\n".join([c for c, _ in context_chunks])
    prompt = f"""
You are a financial analysis assistant. Use the context to answer questions precisely.

Context:
{context}

Question: {query}
Answer:""".strip()
    return prompt

def ask_together(prompt):
    payload = {
        "model": TOGETHER_MODEL,
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.3,
        "top_p": 0.9,
        "stop": ["\n\n"]
    }
    response = requests.post("https://api.together.xyz/v1/completions", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["text"].strip()

