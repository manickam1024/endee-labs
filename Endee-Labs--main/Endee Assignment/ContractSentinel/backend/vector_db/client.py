import os
import requests
import json
from typing import List, Dict, Optional
from backend.schemas import Chunk, SearchResult

class EndeeClient:
    def __init__(self, host: str = "localhost", port: int = 8080):
        self.base_url = f"http://{host}:{port}"
        self.headers = {"Content-Type": "application/json"}
    
    def _get_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def health_check(self) -> bool:
        try:
            response = requests.get(self._get_url("health"), timeout=2)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def create_collection(self, name: str, dimension: int, distance_metric: str = "cosine"):
        """
        Creates a new collection in Endee.
        """
        payload = {
            "name": name,
            "dimension": dimension,
            "metric": distance_metric
        }
        # Note: Actual endpoint might differ based on Endee API spec
        response = requests.post(self._get_url("v1/collections"), json=payload, headers=self.headers)
        if response.status_code not in [200, 201]:
             # If collection already exists, we might get a 409 or similar. 
             # For now, just print error unless it's 'already exists'
             print(f"Warning creating collection: {response.text}")

    def insert_chunks(self, collection_name: str, chunks: List[Chunk]):
        """
        Inserts vectors into the collection.
        """
        data = []
        for chunk in chunks:
            if not chunk.vector:
                continue
            data.append({
                "id": chunk.id,
                "values": chunk.vector,
                "metadata": chunk.metadata,
                "document": chunk.content # Storing content in metadata or separate field dependent on DB
            })
        
        payload = {"vectors": data}
        response = requests.post(self._get_url(f"v1/collections/{collection_name}/insert"), json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def search(self, collection_name: str, query_vector: List[float], limit: int = 5) -> List[SearchResult]:
        """
        Performs a semantic search.
        """
        payload = {
            "vector": query_vector,
            "top_k": limit,
            "include_metadata": True,
            "include_values": False
        }
        
        response = requests.post(self._get_url(f"v1/collections/{collection_name}/search"), json=payload, headers=self.headers)
        response.raise_for_status()
        
        results = response.json().get("results", [])
        search_results = []
        
        for res in results:
            # Adapt this parsing logic to actual Endee response structure
            metadata = res.get("metadata", {})
            content = metadata.get("content") or res.get("document") or ""
            
            search_results.append(SearchResult(
                chunk_id=res.get("id"),
                content=content,
                score=res.get("score", 0.0),
                metadata=metadata
            ))
            
        return search_results
