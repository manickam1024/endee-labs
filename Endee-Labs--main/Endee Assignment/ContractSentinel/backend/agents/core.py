import os
import re
from typing import List, Dict
from backend.agents.tools import AgentTools

# Integration with an actual LLM (OpenAI/Ollama) would go here.
# For this code snippet, I will implement the Logic structure and a mock LLM interface 
# that can be easily swapped.

class MockLLM:
    """
    Simulates LLM responses for demonstration if no API key is present.
    In production, replace with LangChain ChatOpenAI or similar.
    """
    def generate(self, prompt: str) -> str:
        # Simple heuristic to simulate an agent's "Thought" process
        if "liability" in prompt.lower() and "Observation" not in prompt:
            return "Thought: The user is asking about liability. I should search the contract for liability clauses.\nAction: search_contract: liability clauses"
        elif "Observation" in prompt and "liability" in prompt.lower():
             return "Thought: I have found the liability clauses. I should now check the playbook to see if they are risky.\nAction: check_playbook: liability"
        elif "playbook" in prompt.lower() and "Observation" in prompt:
            return "Final Answer: The contract contains liability clauses that cap damages at 2x fees. According to the playbook, this is acceptable but bordering on high risk. I recommend negotiating this down to 1x fees if possible."
        else:
            return "Final Answer: I cannot determine the answer from the available tools."

class ContractAgent:
    def __init__(self):
        self.tools = AgentTools()
        self.llm = MockLLM() # Replace with real LLM client
        self.max_steps = 5
        
    def run(self, user_query: str) -> str:
        """
        Executes the ReAct loop: Thought -> Action -> Observation -> Final Answer
        """
        state_history = f"Question: {user_query}\n"
        
        for step in range(self.max_steps):
            # 1. LLM Thinks
            response = self.llm.generate(state_history)
            state_history += f"{response}\n"
            
            # 2. Check for Final Answer
            if "Final Answer:" in response:
                return response.split("Final Answer:")[1].strip()
            
            # 3. Parse Action
            # Expected format: "Action: tool_name: input"
            action_match = re.search(r"Action: (\w+): (.*)", response)
            if action_match:
                tool_name = action_match.group(1)
                tool_input = action_match.group(2).strip()
                
                # 4. Execute Tool
                observation = self._execute_tool(tool_name, tool_input)
                state_history += f"Observation: {observation}\n"
            else:
                # If LLM messes up format, break or retry
                return "Error: Agent failed to decide on a valid action."
                
        return "Error: Agent reached maximum steps without a final answer."

    def _execute_tool(self, tool_name: str, tool_input: str) -> str:
        if tool_name == "search_contract":
            return self.tools.search_contract(tool_input)
        elif tool_name == "check_playbook":
            return self.tools.check_playbook(tool_input)
        else:
            return f"Error: Tool '{tool_name}' not found."
