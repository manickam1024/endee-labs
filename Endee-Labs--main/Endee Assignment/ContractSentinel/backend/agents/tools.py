from typing import List, Dict
from backend.retrieval.engine import RetrievalEngine

class AgentTools:
    def __init__(self):
        self.retriever = RetrievalEngine()

    def search_contract(self, query: str) -> str:
        """
        Searches the ingested contract for clauses relevant to the query.
        Returns a formatted string of the top results.
        """
        try:
            results = self.retriever.search(query, limit=3)
            if not results:
                return "No relevant clauses found in the contract."
            
            formatted_results = "Here are the relevant contract clauses found:\n"
            for i, res in enumerate(results, 1):
                formatted_results += f"{i}. [Score: {res.score:.2f}] {res.content}\n\n"
            return formatted_results
        except Exception as e:
            return f"Error executing search: {str(e)}"

    def check_playbook(self, risk_type: str) -> str:
        """
        Simulates looking up a legal playbook for standard risk positions.
        """
        playbook = {
            "liability": "Standard liability cap should be 12 months fees. Super caps > 2x fees are high risk.",
            "indemnification": "Indemnification should be mutual. Unilateral indemnification is high risk.",
            "termination": "Termination for convenience should hold a 30-day notice period.",
            "jurisdiction": "Preferred jurisdiction is Delaware or New York."
        }
        return playbook.get(risk_type.lower(), "No specific playbook entry for this risk type.")
