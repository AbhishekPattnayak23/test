"""
Vector Store module for CV Villas Agent Assist.

This module provides a unified interface for semantic similarity search using FAISS
with an in-memory fallback store for development/testing scenarios.
"""
import faiss
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import logging
import pickle
from enum import Enum
from dataclasses import dataclass
import asyncio
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


class VectorStoreType(Enum):
    """Types of vector stores supported."""
    FAISS = "faiss"
    IN_MEMORY = "in_memory"
    POSTGRES_PGVECTOR = "pgvector"


@dataclass
class SearchResult:
    """Result from vector similarity search."""
    knowledge_source_id: str
    relevance_score: float
    snippet_text: str
    metadata: Dict[str, Any]


class BaseVectorStore:
    """Base abstract class for vector stores."""
    
    async def initialize(self) -> None:
        """Initialize the vector store."""
        raise NotImplementedError
    
    async def add_embeddings(
        self, 
        embeddings: List[np.ndarray],
        metadata: List[Dict[str, Any]]
    ) -> List[str]:
        """Add embeddings to the store."""
        raise NotImplementedError
    
    async def search(
        self, 
        query_embedding: np.ndarray, 
        k: int = 5
    ) -> List[SearchResult]:
        """Search for similar embeddings."""
        raise NotImplementedError
    
    async def remove(self, ids: List[str]) -> None:
        """Remove embeddings by IDs."""
        raise NotImplementedError
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        raise NotImplementedError
    
    def get_store_type(self) -> str:
        """Get the type of this vector store."""
        raise NotImplementedError


class FAISSVectorStore(BaseVectorStore):
    """FAISS-based vector store using in-memory index."""
    
    def __init__(self, dimension: int = 384):
        """
        Initialize FAISS vector store.
        
        Args:
            dimension: Dimension of embeddings (default: 384 for all-MiniLM-L6-v2)
        """
        self.dimension = dimension
        self.index = None
        self.ids = []  # List of knowledge source IDs
        self.metadata = {}  # Mapping from ID to metadata
        
    async def initialize(self) -> None:
        """Initialize FAISS index."""
        if self.index is None:
            # Create a flat L2 index (exact search)
            self.index = faiss.IndexFlatL2(self.dimension)
            logger.info(f"Initialized FAISS index with dimension {self.dimension}")
        
    async def add_embeddings(
        self, 
        embeddings: List[np.ndarray],
        metadata: List[Dict[str, Any]]
    ) -> List[str]:
        """Add embeddings to FAISS index."""
        if not embeddings:
            return []
        
        # Ensure embeddings are the right shape
        embeddings_array = np.array(embeddings).astype('float32')
        
        if embeddings_array.shape[1] != self.dimension:
            raise ValueError(
                f"Embedding dimension mismatch: expected {self.dimension}, "
                f"got {embeddings_array.shape[1]}"
            )
        
        # Generate IDs for new embeddings
        start_id = len(self.ids)
        new_ids = [f"ks_{start_id + i}" for i in range(len(embeddings))]
        
        # Add to index
        self.index.add(embeddings_array)
        
        # Store IDs and metadata
        self.ids.extend(new_ids)
        for idx, md in enumerate(metadata):
            self.metadata[new_ids[idx]] = md
        
        logger.info(f"Added {len(new_ids)} embeddings to FAISS index")
        return new_ids
    
    async def search(
        self, 
        query_embedding: np.ndarray, 
        k: int = 5
    ) -> List[SearchResult]:
        """Search FAISS index for similar embeddings."""
        if self.index is None or self.index.ntotal == 0:
            return []
        
        # Prepare query
        query_array = np.array([query_embedding]).astype('float32')
        
        # Search
        distances, indices = self.index.search(query_array, min(k, self.index.ntotal))
        
        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            if idx >= 0 and idx < len(self.ids):
                knowledge_source_id = self.ids[idx]
                distance = distances[0][i]
                
                # Convert distance to relevance score (inverse of distance)
                # Add small epsilon to avoid division by zero
                relevance_score = 1.0 / (1.0 + distance)
                
                metadata = self.metadata.get(knowledge_source_id, {})
                snippet_text = metadata.get('snippet', '')
                
                results.append(SearchResult(
                    knowledge_source_id=knowledge_source_id,
                    relevance_score=relevance_score,
                    snippet_text=snippet_text,
                    metadata=metadata
                ))
        
        return results
    
    async def remove(self, ids: List[str]) -> None:
        """Remove embeddings by IDs - not efficient for FAISS."""
        # FAISS doesn't support efficient removal, so we mark as removed in metadata
        for ks_id in ids:
            if ks_id in self.metadata:
                self.metadata[ks_id]['removed'] = True
                logger.info(f"Marked embedding {ks_id} as removed")
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the FAISS index."""
        total = self.index.ntotal if self.index else 0
        dimension = self.dimension
        
        return {
            "store_type": "faiss",
            "total_embeddings": total,
            "dimension": dimension,
            "index_type": "IndexFlatL2",
            "metadata_count": len(self.metadata)
        }
    
    def get_store_type(self) -> str:
        """Get store type."""
        return VectorStoreType.FAISS.value


class FallbackStore(BaseVectorStore):
    """
    In-memory fallback store for development/testing.
    
    Uses simple cosine similarity calculation without FAISS dependency.
    """
    
    def __init__(self):
        self.embeddings = []  # List of numpy arrays
        self.ids = []  # List of knowledge source IDs
        self.metadata = {}  # Mapping from ID to metadata
        
    async def initialize(self) -> None:
        """Initialize the fallback store."""
        logger.info("Initialized in-memory fallback vector store")
    
    async def add_embeddings(
        self, 
        embeddings: List[np.ndarray],
        metadata: List[Dict[str, Any]]
    ) -> List[str]:
        """Add embeddings to in-memory store."""
        if not embeddings:
            return []
        
        # Generate IDs
        start_id = len(self.ids)
        new_ids = [f"fallback_{start_id + i}" for i in range(len(embeddings))]
        
        # Store embeddings and metadata
        self.embeddings.extend(embeddings)
        self.ids.extend(new_ids)
        for idx, md in enumerate(metadata):
            self.metadata[new_ids[idx]] = md
        
        logger.info(f"Added {len(new_ids)} embeddings to fallback store")
        return new_ids
    
    async def search(
        self, 
        query_embedding: np.ndarray, 
        k: int = 5
    ) -> List[SearchResult]:
        """Search using cosine similarity."""
        if not self.embeddings:
            return []
        
        # Calculate cosine similarities
        query_norm = np.linalg.norm(query_embedding)
        similarities = []
        
        for idx, embedding in enumerate(self.embeddings):
            if self.metadata.get(self.ids[idx], {}).get('removed', False):
                continue
                
            embedding_norm = np.linalg.norm(embedding)
            if query_norm > 0 and embedding_norm > 0:
                similarity = np.dot(query_embedding, embedding) / (query_norm * embedding_norm)
                similarities.append((idx, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for idx, (embedding_idx, similarity) in enumerate(similarities[:k]):
            knowledge_source_id = self.ids[embedding_idx]
            metadata = self.metadata.get(knowledge_source_id, {})
            snippet_text = metadata.get('snippet', '')
            
            results.append(SearchResult(
                knowledge_source_id=knowledge_source_id,
                relevance_score=max(0.0, similarity),  # Ensure non-negative
                snippet_text=snippet_text,
                metadata=metadata
            ))
        
        return results
    
    async def remove(self, ids: List[str]) -> None:
        """Remove embeddings by marking them as removed."""
        for ks_id in ids:
            if ks_id in self.metadata:
                self.metadata[ks_id]['removed'] = True
                logger.info(f"Marked embedding {ks_id} as removed in fallback store")
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the fallback store."""
        total = len(self.embeddings)
        active = sum(1 for ks_id in self.ids 
                    if not self.metadata.get(ks_id, {}).get('removed', False))
        
        return {
            "store_type": "fallback",
            "total_embeddings": total,
            "active_embeddings": active,
            "dimension": self.embeddings[0].shape[0] if self.embeddings else 0,
            "storage": "in_memory"
        }
    
    def get_store_type(self) -> str:
        """Get store type."""
        return VectorStoreType.IN_MEMORY.value


class VectorStoreManager:
    """
    Manager class that provides a unified interface to vector stores,
    with automatic fallback to in-memory store if FAISS is not available.
    """
    
    def __init__(self):
        self.primary_store = None
        self.fallback_store = None
        
    async def initialize(self) -> None:
        """Initialize vector store with fallback mechanism."""
        try:
            # Try to initialize FAISS store
            self.primary_store = FAISSVectorStore(dimension=384)
            await self.primary_store.initialize()
            logger.info("FAISS vector store initialized successfully")
        except ImportError as e:
            logger.warning(f"FAISS not available: {e}. Using fallback store.")
            self.fallback_store = FallbackStore()
            await self.fallback_store.initialize()
        except Exception as e:
            logger.error(f"Error initializing FAISS: {e}. Using fallback store.")
            self.fallback_store = FallbackStore()
            await self.fallback_store.initialize()
    
    def get_active_store(self) -> BaseVectorStore:
        """Get the currently active vector store."""
        if self.primary_store:
            return self.primary_store
        elif self.fallback_store:
            return self.fallback_store
        else:
            raise RuntimeError("No vector store initialized")
    
    async def add_embeddings(
        self, 
        embeddings: List[np.ndarray],
        metadata: List[Dict[str, Any]]
    ) -> List[str]:
        """Add embeddings to the active store."""
        store = self.get_active_store()
        return await store.add_embeddings(embeddings, metadata)
    
    async def search(
        self, 
        query_embedding: np.ndarray, 
        k: int = 5
    ) -> List[SearchResult]:
        """Search the active store for similar embeddings."""
        store = self.get_active_store()
        return await store.search(query_embedding, k)
    
    async def remove(self, ids: List[str]) -> None:
        """Remove embeddings from the active store."""
        store = self.get_active_store()
        return await store.remove(ids)
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get statistics from the active store."""
        store = self.get_active_store()
        return await store.get_stats()
    
    def get_store_type(self) -> str:
        """Get the type of the active store."""
        store = self.get_active_store()
        return store.get_store_type()


# Singleton instance
_vector_store_manager = None


def get_vector_store() -> VectorStoreManager:
    """Get the singleton vector store instance."""
    global _vector_store_manager
    
    if _vector_store_manager is None:
        _vector_store_manager = VectorStoreManager()
    
    return _vector_store_manager