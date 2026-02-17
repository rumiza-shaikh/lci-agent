"""
LCI Agent - Universal Context Infrastructure for AI
Version 0.1.0 - Day 1
"""

from anthropic import Anthropic
import os
from pathlib import Path
from typing import List, Dict

class LCIAgent:
    """
    The LCI Agent - Context Intelligence for AI
    """
    
    def __init__(self, api_key: str = None):
        """Initialize the agent"""
        self.client = Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY")
        )
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
                
                # Simple relevance check (we'll improve this)
                if any(word.lower() in content.lower() 
                       for word in query.split()):
                    context.append({
                        "source": file.name,
                        "content": content[:1000],  # First 1000 chars
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
            sources: List of sources to use (default: ["local"])
            
        Returns:
            Dict with context, response, and metadata
        """
        # Step 1: Get context
        context_items = self.get_local_context(query)
        
        if not context_items:
            return {
                "query": query,
                "context": [],
                "response": "No relevant context found.",
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

Please answer based on the local context provided. Always cite which source you used.
If the context doesn't contain the answer, say so clearly."""
        
        # Step 3: Call LLM
        message = self.client.messages.create(
            model="gemini-1.5-flash",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        # Step 4: Return structured response
        return {
            "query": query,
            "context": context_items,
            "response": response_text,
            "sources_checked": ["local"],
            "sources_used": [item["source"] for item in context_items],
            "model": "claude-sonnet-4",
            "timestamp": "2026-02-15"  # We'll make this dynamic later
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
        print(f"\n📄 {item['source']}")
        print(f"   {item['content'][:200]}...")
    
    print("\n" + "=" * 50)
    print("RESPONSE:")
    print("=" * 50)
    print(result["response"])
    
    print("\n" + "=" * 50)
    print(f"Sources used: {', '.join(result['sources_used'])}")
