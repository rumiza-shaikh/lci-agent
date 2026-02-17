"""
LCI Agent - Universal Context Infrastructure for AI
Version 0.1.0 - Day 1
Powered by Google Gemini (Free)
"""

import google.generativeai as genai
import os
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LCIAgent:
    """
    The LCI Agent - Context Intelligence for AI
    """
    
    def __init__(self, api_key: str = None):
        """Initialize the agent"""
        # Configure Gemini
        genai.configure(
            api_key=api_key or os.environ.get("GEMINI_API_KEY")
        )
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.context_dir = Path("./context_data")
        self.context_dir.mkdir(exist_ok=True)
    
    def get_local_context(self, query: str) -> List[Dict]:
        """
        Retrieve context from local files
        
        Args:
            query: User's question
            
        Returns:
            List of context items with source and content
        """
        context = []
        
        # Get all text files
        for file in self.context_dir.glob("*.txt"):
            with open(file, 'r') as f:
                content = f.read()
                
                # Simple relevance check
                if any(word.lower() in content.lower() 
                       for word in query.split()):
                    context.append({
                        "source": file.name,
                        "content": content[:1000],
                        "type": "local_file"
                    })
        
        return context
    
    def retrieve_context(self, 
                        query: str,
                        sources: List[str] = None) -> Dict:
        """
        Main method - retrieve context and ground the response
        
        Args:
            query: User's question
            sources: List of sources to use
            
        Returns:
            Dict with context, response, and metadata
        """
        # Step 1: Get local context
        context_items = self.get_local_context(query)
        
        if not context_items:
            return {
                "query": query,
                "context": [],
                "response": "No relevant context found in local files.",
                "sources_checked": ["local"],
                "sources_used": []
            }
        
        # Step 2: Build prompt with context
        context_text = "\n\n".join([
            f"Source: {item['source']}\n{item['content']}"
            for item in context_items
        ])
        
        prompt = f"""You are an AI assistant with access to local context.

Local Context Available:
{context_text}

User Query: {query}

Please answer based ONLY on the local context provided. 
Always cite which source you used.
If the context doesn't contain the answer, say so clearly."""
        
        # Step 3: Call Gemini
        response = self.model.generate_content(prompt)
        response_text = response.text
        
        # Step 4: Return structured response
        return {
            "query": query,
            "context": context_items,
            "response": response_text,
            "sources_checked": ["local"],
            "sources_used": [item["source"] for item in context_items],
            "model": "gemini-1.5-flash",
            "timestamp": "2026-02-16"
        }


# Simple CLI interface
if __name__ == "__main__":
    import sys
    
    # Initialize agent
    agent = LCIAgent()
    
    # Create sample context if none exists
    sample_file = agent.context_dir / "sample.txt"
    if not sample_file.exists():
        sample_file.write_text(
            "GSTIN filing for LLPs in Maharashtra is quarterly "
            "for entities with turnover under 5 Crores."
        )
        print("✓ Created sample context file")
    
    # Get query from command line or use default
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
            "What are the GSTIN filing rules?"
    
    print(f"\nQuery: {query}\n")
    
    # Retrieve context
    result = agent.retrieve_context(query)
    
    # Print results
    print("=" * 50)
    print("CONTEXT RETRIEVED:")
    print("=" * 50)
    for item in result["context"]:
        print(f"\n📄 Source: {item['source']}")
        print(f"   {item['content'][:200]}...")
    
    print("\n" + "=" * 50)
    print("LCI AGENT RESPONSE:")
    print("=" * 50)
    print(result["response"])
    
    print("\n" + "=" * 50)
    print(f"✓ Model: {result['model']}")
    print(f"✓ Sources used: {', '.join(result['sources_used'])}")
    print(f"✓ Sources checked: {', '.join(result['sources_checked'])}")
