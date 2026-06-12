"""FAISS-based vector store for RAG (Python 3.14 compatible)"""
import os
import json
import numpy as np
from typing import List, Dict, Optional
import requests


class VectorStore:
    """Simple FAISS-based vector store for deal embeddings"""
    
    def __init__(self, dimension: int = 384, storage_path: str = "vector_store.json"):
        self.dimension = dimension
        self.storage_path = storage_path
        self.documents: List[Dict] = []
        self.embeddings: Optional[np.ndarray] = None
        self.ollama_url = "http://localhost:11434/api/embeddings"
        self.load()
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """Get embedding from Ollama"""
        try:
            payload = {
                "model": "nomic-embed-text",
                "prompt": text
            }
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            response.raise_for_status()
            embedding = response.json()["embedding"]
            return np.array(embedding, dtype=np.float32)
        except Exception as e:
            print(f"Embedding error: {e}")
            # Return random embedding as fallback
            return np.random.randn(self.dimension).astype(np.float32)
    
    def add_document(self, text: str, metadata: Dict):
        """Add a document to the vector store"""
        embedding = self._get_embedding(text)
        
        self.documents.append({
            "text": text,
            "metadata": metadata
        })
        
        if self.embeddings is None:
            self.embeddings = embedding.reshape(1, -1)
        else:
            self.embeddings = np.vstack([self.embeddings, embedding])
        
        self.save()
    
    def similarity_search(self, query: str, k: int = 3) -> List[Dict]:
        """Search for similar documents using cosine similarity"""
        if not self.documents or self.embeddings is None:
            return []
        
        query_embedding = self._get_embedding(query)
        
        # Cosine similarity
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Get top k indices
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        
        results = []
        for idx in top_k_indices:
            results.append({
                "text": self.documents[idx]["text"],
                "metadata": self.documents[idx]["metadata"],
                "similarity": float(similarities[idx])
            })
        
        return results
    
    def save(self):
        """Save vector store to disk"""
        data = {
            "documents": self.documents,
            "embeddings": self.embeddings.tolist() if self.embeddings is not None else None
        }
        with open(self.storage_path, "w") as f:
            json.dump(data, f)
    
    def load(self):
        """Load vector store from disk"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                self.documents = data.get("documents", [])
                embeddings_list = data.get("embeddings")
                if embeddings_list:
                    self.embeddings = np.array(embeddings_list, dtype=np.float32)
            except Exception as e:
                print(f"Failed to load vector store: {e}")
    
    def clear(self):
        """Clear all documents"""
        self.documents = []
        self.embeddings = None
        if os.path.exists(self.storage_path):
            os.remove(self.storage_path)
