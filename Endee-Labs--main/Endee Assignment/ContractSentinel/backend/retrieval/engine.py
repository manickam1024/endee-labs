import os
from typing import List
from backend.vector_db.client import EndeeClient
from backend.embeddings.model import EmbeddingModel
from backend.schemas import SearchResult

class RetrievalEngine:
    def __init__(self):
        self.db_client = EndeeClient(
            host=os.getenv("ENDEE_HOST", "localhost"),
            port=int(os.getenv("ENDEE_PORT", 8080))
        )
        self.embedder = EmbeddingModel()
        self.collection_name = "contracts"

    def search(self, query: str, limit: int = 5) -> List[SearchResult]:
        """
        Embeds the query and searches the vector database.
        """
        print(f"Searching for: {query}")
        query_vector = self.embedder.embed_text(query)
        results = self.db_client.search(self.collection_name, query_vector, limit=limit)
        return results

    def hybrid_search(self, query: str):
        # Placeholder for hybrid search if Endee supports it or if we implement BM25 locally
        pass
