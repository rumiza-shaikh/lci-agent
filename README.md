# LCI Agent

**Universal context infrastructure for AI applications**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Status](https://img.shields.io/badge/status-experimental-orange)

## What is LCI Agent?

LCI Agent provides context intelligence infrastructure for AI applications. It retrieves local, relevant, and verified context from multiple sources and grounds LLM responses in your specific data.

### Key Features

- 🎯 **Deterministic**: Same query + same context = same answer
- 🔒 **Privacy-first**: Local processing, PII masking, zero retention
- 📚 **Multi-source**: Drive, Slack, local files, and more
- 🔗 **Universal**: Works with any LLM (OpenAI, Anthropic, etc.)
- ⚡ **Fast**: Parallel retrieval, optimized for <500ms latency

## Quick Start
```bash
# Install
pip install lci-agent

# Start the agent
lci-agent start

# Use the API
curl -X POST http://localhost:8000/context/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query": "What are my tax filing rules?"}'
```

## Example
```python
from lci_agent import get_context

# Retrieve context from multiple sources
context = get_context(
    query="What are the GSTIN filing rules for my business?",
    sources=["drive", "local"],
    privacy="local-first"
)

print(context)
# Returns: grounded context with citations
```

## Architecture
```
User Query → LCI Agent → Context Retrieval → LLM → Grounded Response
                ↓
         [Drive, Slack, Files, APIs]
```

## Why LCI Agent?

**The Problem:**
- LLMs are brilliant at general reasoning
- But they fail at specific, local, compliant tasks
- Every team rebuilds context retrieval from scratch

**The Solution:**
- Universal context infrastructure
- Plug into any application
- Deterministic, privacy-preserving, auditable

## Status

⚠️ **Early prototype** - Built as a research project exploring context intelligence patterns.

Currently implementing:
- [x] Basic API structure
- [x] Local file connector
- [ ] Google Drive connector
- [ ] Privacy controls (PII masking)
- [ ] Audit logging
- [ ] Additional connectors

## Roadmap

**Week 1-2:**
- Core API endpoints
- Google Drive + Slack connectors
- Basic privacy features

**Week 3-4:**
- Advanced retrieval (semantic search)
- Context grounding and citations
- Audit trails

**Week 5+:**
- Community contributions
- More connectors
- Production hardening

## Contributing

This is a learning project built in public. Contributions welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Use Cases

- **Enterprise AI**: Ground copilots in company-specific data
- **Compliance**: Ensure AI uses only approved sources
- **Personal AI**: Give AI access to your local context
- **Developer tools**: Build context-aware dev assistants

## Tech Stack

- **API**: FastAPI (Python)
- **LLMs**: OpenAI, Anthropic Claude, local models
- **Connectors**: Google Drive, Slack, local files
- **Storage**: FAISS for vector search (lightweight)

## About

Built by [Rumiza Shaikh](https://linkedin.com/in/yourprofile) as part of research into Local Context Intelligence.

Exploring how to make AI systems understand specific, local, recent context while maintaining privacy and compliance.

Not affiliated with any company. Open source, community-driven.

## License

MIT License - use freely!

## Links

- [LinkedIn](https://www.linkedin.com/in/rumiza-shaikh/) - Follow my build-in-public journey
- [Issues](https://github.com/rumiza-shaikh/lci-agent/issues) - Report bugs or request features
- [Discussions](https://github.com/rumiza-shaikh/lci-agent/discussions) - Join the conversation
- I build in public on Linkedin and X - (https://x.com/RTweetsOnX)

---

**Built with ❤️ and Claude** 

*Last updated: February 2026*
