import os
from dotenv import load_dotenv

# Load .env BEFORE creating the client
load_dotenv()

import faiss
import numpy as np
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class KnowledgeBase:
    def __init__(self):
        self.index = None
        self.text_chunks = []

    # Convert text chunk → embedding
    def create_embedding(self, text):
        emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return np.array(emb.data[0].embedding, dtype="float32")

    # Load text file + build vector DB
    def load_knowledge(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = text.split("\n")
        self.text_chunks = chunks

        embeddings = [self.create_embedding(chunk) for chunk in chunks]
        embedding_dim = len(embeddings[0])

        self.index = faiss.IndexFlatL2(embedding_dim)
        self.index.add(np.array(embeddings))

    # Find similar chunks
    def search(self, query, top_k=3):
        q_emb = self.create_embedding(query)
        D, I = self.index.search(np.array([q_emb]), top_k)
        results = [self.text_chunks[i] for i in I[0]]
        return results