from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from uuid import uuid4

class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str
    metadata: Dict[str, Any] = {}

class Chunk(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    document_id: str
    content: str
    vector: Optional[List[float]] = None
    metadata: Dict[str, Any] = {}

class SearchResult(BaseModel):
    chunk_id: str
    content: str
    score: float
    metadata: Dict[str, Any] = {}
