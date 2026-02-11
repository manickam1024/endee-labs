import os
from typing import List, Optional
from pypdf import PdfReader
from backend.ingestion.chunking import RecursiveTokenChunker
from backend.vector_db.client import EndeeClient
from backend.embeddings.model import EmbeddingModel
from backend.schemas import Document, Chunk

class IngestionPipeline:
    def __init__(self):
        self.chunker = RecursiveTokenChunker(chunk_size=512, chunk_overlap=50) # Approx tokens
        self.db_client = EndeeClient(
            host=os.getenv("ENDEE_HOST", "localhost"),
            port=int(os.getenv("ENDEE_PORT", 8080))
        )
        self.embedder = EmbeddingModel()
        self.collection_name = "contracts" # Default collection

    def ensure_collection(self):
        # Create collection if arguably not exists (Endee client handles check loosely)
        self.db_client.create_collection(
            name=self.collection_name, 
            dimension=self.embedder.dimension
        )

    def process_pdf(self, file_path: str) -> str:
        """
        Reads PDF, chunks it, embeds it, and indexes it.
        Returns the Document ID.
        """
        print(f"Processing PDF: {file_path}")
        reader = PdfReader(file_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        
        doc = Document(content=full_text, metadata={"source": file_path})
        
        # Chunking
        text_chunks = self.chunker.split_text(full_text)
        print(f"Generated {len(text_chunks)} chunks.")

        # Embedding & Object Creation
        chunks_to_persist = []
        vectors = self.embedder.embed_batch(text_chunks)
        
        for i, text in enumerate(text_chunks):
            chunk_obj = Chunk(
                document_id=doc.id,
                content=text,
                vector=vectors[i],
                metadata={
                    "order": i,
                    "source": file_path
                }
            )
            chunks_to_persist.append(chunk_obj)
        
        # Indexing
        self.ensure_collection()
        self.db_client.insert_chunks(self.collection_name, chunks_to_persist)
        print("Ingestion complete.")
        return doc.id
