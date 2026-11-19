"""
Vector store service for CV Villas Knowledge Assistant.
Provides FAISS-based vector similarity search with in-memory fallback.
"""

import json
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("FAISS not available, using fallback in-memory store")

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    logger.warning("Sentence transformers not available, using mock embeddings")


class VectorStore:
    """Base vector store interface."""
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.documents = {}  # Map from vector index to document metadata
        self.next_id = 0
        
    def add_documents(self, documents: List[Dict[str, Any]], embeddings: Optional[List[List[float]]] = None) -> List[int]:
        """Add documents to the vector store."""
        raise NotImplementedError
    
    def search(self, query_vector: List[float], k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        raise NotImplementedError
    
    def delete_all(self) -> None:
        """Delete all vectors from the store."""
        raise NotImplementedError
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        raise NotImplementedError


class FAISSVectorStore(VectorStore):
    """FAISS-based vector store for production use."""
    
    def __init__(self, dimension: int = 384, index_type: str = "FlatL2"):
        super().__init__(dimension)
        
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS is not installed. Install with `pip install faiss-cpu`")
        
        # Initialize FAISS index
        if index_type == "FlatL2":
            self.index = faiss.IndexFlatL2(dimension)
        else:
            self.index = faiss.IndexFlatL2(dimension)  # Default to FlatL2
        
        logger.info(f"Initialized FAISS vector store with dimension {dimension}")
    
    def add_documents(self, documents: List[Dict[str, Any]], embeddings: Optional[List[List[float]]] = None) -> List[int]:
        """Add documents to FAISS index."""
        if not documents:
            return []
        
        # Generate embeddings if not provided
        if embeddings is None:
            embeddings = self._generate_embeddings([doc.get("text", "") for doc in documents])
        
        # Convert to numpy array
        vectors = np.array(embeddings).astype('float32')
        
        # Add to index
        self.index.add(vectors)
        
        # Store document metadata
        start_id = self.next_id
        for i, doc in enumerate(documents):
            doc_id = self.next_id + i
            self.documents[doc_id] = {
                **doc,
                "vector_id": doc_id,
                "added_at": datetime.utcnow().isoformat()
            }
        
        self.next_id += len(documents)
        
        logger.info(f"Added {len(documents)} documents to FAISS store")
        return list(range(start_id, self.next_id))
    
    def search(self, query_vector: List[float], k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents using FAISS."""
        if self.index.ntotal == 0:
            return []
        
        # Convert query vector to numpy array
        query = np.array([query_vector]).astype('float32')
        
        # Search
        distances, indices = self.index.search(query, min(k, self.index.ntotal))
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx >= 0:  # Valid index
                doc = self.documents.get(idx)
                if doc:
                    results.append({
                        **doc,
                        "distance": float(distance),
                        "similarity_score": 1.0 / (1.0 + distance)  # Convert distance to similarity
                    })
        
        return results
    
    def delete_all(self) -> None:
        """Delete all vectors from FAISS index."""
        self.index.reset()
        self.documents.clear()
        self.next_id = 0
        logger.info("Cleared FAISS vector store")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the FAISS store."""
        return {
            "total_vectors": self.index.ntotal,
            "dimension": self.dimension,
            "next_id": self.next_id,
            "store_type": "FAISS"
        }
    
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts."""
        if EMBEDDINGS_AVAILABLE:
            # Use sentence-transformers if available
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embeddings = model.encode(texts)
            return embeddings.tolist()
        else:
            # Mock embeddings for development
            return [[float(i) / 1000.0 for _ in range(self.dimension)] for i in range(len(texts))]


class FallbackStore(VectorStore):
    """In-memory fallback vector store for when FAISS is not available."""
    
    def __init__(self, dimension: int = 384):
        super().__init__(dimension)
        self.vectors = []  # List of vectors
        logger.info(f"Initialized fallback vector store with dimension {dimension}")
    
    def add_documents(self, documents: List[Dict[str, Any]], embeddings: Optional[List[List[float]]] = None) -> List[int]:
        """Add documents to in-memory store."""
        if not documents:
            return []
        
        # Generate embeddings if not provided
        if embeddings is None:
            embeddings = self._generate_embeddings([doc.get("text", "") for doc in documents])
        
        # Store vectors and documents
        start_id = self.next_id
        for i, (doc, emb) in enumerate(zip(documents, embeddings)):
            doc_id = self.next_id + i
            self.vectors.append(emb)
            self.documents[doc_id] = {
                **doc,
                "vector_id": doc_id,
                "added_at": datetime.utcnow().isoformat()
            }
        
        self.next_id += len(documents)
        
        logger.info(f"Added {len(documents)} documents to fallback store")
        return list(range(start_id, self.next_id))
    
    def search(self, query_vector: List[float], k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents using cosine similarity."""
        if not self.vectors:
            return []
        
        # Calculate cosine similarity
        query_norm = np.linalg.norm(query_vector)
        results = []
        
        for i, vector in enumerate(self.vectors):
            if i in self.documents:
                # Calculate cosine similarity
                dot_product = np.dot(query_vector, vector)
                vector_norm = np.linalg.norm(vector)
                
                if query_norm > 0 and vector_norm > 0:
                    similarity = dot_product / (query_norm * vector_norm)
                else:
                    similarity = 0.0
                
                results.append({
                    **self.documents[i],
                    "distance": 1.0 - similarity,  # Convert to distance
                    "similarity_score": similarity
                })
        
        # Sort by similarity (descending) and take top k
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:k]
    
    def delete_all(self) -> None:
        """Delete all vectors from memory."""
        self.vectors.clear()
        self.documents.clear()
        self.next_id = 0
        logger.info("Cleared fallback vector store")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the fallback store."""
        return {
            "total_vectors": len(self.vectors),
            "dimension": self.dimension,
            "next_id": self.next_id,
            "store_type": "Fallback"
        }
    
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate mock embeddings for texts."""
        # Simple deterministic mock embeddings
        return [[float(hash(text) % 1000) / 1000.0 for _ in range(self.dimension)] for text in texts]


class VectorStoreFactory:
    """Factory for creating vector stores."""
    
    @staticmethod
    def create_vector_store(dimension: int = 384, force_fallback: bool = False) -> VectorStore:
        """
        Create a vector store instance.
        
        Args:
            dimension: Dimension of embeddings
            force_fallback: Force using fallback store even if FAISS is available
            
        Returns:
            VectorStore instance
        """
        if FAISS_AVAILABLE and not force_fallback:
            try:
                return FAISSVectorStore(dimension=dimension)
            except Exception as e:
                logger.warning(f"Failed to create FAISS store: {e}. Falling back to in-memory store.")
                return FallbackStore(dimension=dimension)
        else:
            logger.info("Using fallback vector store (FAISS not available or forced)")
            return FallbackStore(dimension=dimension)


# Singleton instance for application use
_vector_store_instance: Optional[VectorStore] = None


def get_vector_store(dimension: int = 384) -> VectorStore:
    """
    Get or create singleton vector store instance.
    
    Args:
        dimension: Dimension of embeddings
        
    Returns:
        VectorStore instance
    """
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStoreFactory.create_vector_store(dimension=dimension)
    return _vector_store_instance


def reset_vector_store() -> None:
    """Reset the singleton vector store instance."""
    global _vector_store_instance
    if _vector_store_instance:
        _vector_store_instance.delete_all()
    _vector_store_instance = None


# Example usage
if __name__ == "__main__":
    # Test the vector store
    store = get_vector_store()
    
    # Add some test documents
    test_docs = [
        {"id": 1, "text": "Villa check-in time is 4:00 PM", "type": "faq"},
        {"id": 2, "text": "Pets are allowed in pet-friendly villas only", "type": "policy"},
        {"id": 3, "text": "Cancellation policy: 30 days for full refund", "type": "policy"},
        {"id": 4, "text": "Villa Serenity has private pool and jacuzzi", "type": "amenity_detail"},
        {"id": 5, "text": "Damage deposit is €1000 refundable", "type": "policy"}
    ]
    
    print("Adding documents...")
    doc_ids = store.add_documents(test_docs)
    print(f"Added {len(doc_ids)} documents")
    
    # Test search
    print("\nTesting search...")
    # Mock query embedding
    query_embedding = [0.1] * 384
    results = store.search(query_embedding, k=3)
    
    print(f"Found {len(results)} results:")
    for result in results:
        print(f"  - {result.get('text', '')[:50]}... (score: {result.get('similarity_score', 0):.3f})")
    
    # Get stats
    stats = store.get_stats()
    print(f"\nStore stats: {stats}")