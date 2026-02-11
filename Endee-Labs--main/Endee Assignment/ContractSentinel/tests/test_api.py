from fastapi.testclient import TestClient
from backend.main import app
import os
import unittest
from unittest.mock import MagicMock, patch

client = TestClient(app)

class TestAPI(unittest.TestCase):
    
    @patch("backend.main.ingest_pipeline")
    def test_ingest_endpoint(self, mock_pipeline):
        # Mock the pipeline return value
        mock_pipeline.process_pdf.return_value = "doc_123"
        
        # Create a dummy PDF content
        files = {"file": ("test.pdf", b"%PDF-1.4 dummy content", "application/pdf")}
        
        response = client.post("/ingest", files=files)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["document_id"], "doc_123")
        self.assertEqual(response.json()["status"], "success")

    @patch("backend.main.agent")
    def test_chat_endpoint(self, mock_agent):
        # Mock the agent response
        mock_agent.run.return_value = "This is a mocked agent response."
        
        payload = {"query": "What is the liability cap?"}
        response = client.post("/chat", json=payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["response"], "This is a mocked agent response.")

    def test_health_check(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "service": "ContractSentinel"})

if __name__ == '__main__':
    unittest.main()
