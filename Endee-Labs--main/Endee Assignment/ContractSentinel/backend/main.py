from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
from backend.ingestion.pipeline import IngestionPipeline
from backend.agents.core import ContractAgent

app = FastAPI(title="ContractSentinel API", version="1.0.0")

# Initialize Singletons
ingest_pipeline = IngestionPipeline()
agent = ContractAgent()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def health_check():
    return {"status": "ok", "service": "ContractSentinel"}

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Uploads a PDF, chunks it, and indexes it into Endee.
    """
    file_location = f"temp_{file.filename}"
    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        
        doc_id = ingest_pipeline.process_pdf(file_location)
        
        # Cleanup
        os.remove(file_location)
        
        return {"status": "success", "document_id": doc_id, "message": "Document ingested successfully."}
    except Exception as e:
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def agent_chat(request: ChatRequest):
    """
    Agentic chat endpoint.
    """
    try:
        response = agent.run(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
