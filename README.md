# Multi-Agent Deal Discovery System

> An intelligent AI system that autonomously discovers product deals, estimates market prices, and identifies bargains using local LLM inference.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Gemma_2B-green.svg)](https://ollama.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

A production-ready multi-agent system that leverages **Gemma 2B** for intelligent deal analysis. Built with clean architecture principles and modern AI techniques.

**Key Achievement:** Implements hierarchical multi-agent architecture with local LLM inference - no cloud APIs required.

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents (Scanner, Ensemble, Planning, Specialist, Messaging)
- **Local AI Processing**: Ollama + Gemma 2B (privacy-focused, zero API costs)
- **Web Interface**: Modern Gradio-based UI for real-time interaction
- **Persistent Memory**: JSON-based storage with deduplication
- **Autonomous Workflow**: End-to-end deal discovery and analysis

## 🏗️ Architecture

```
Framework → Planning Agent → Scanner | Ensemble | Messaging
                                ↓
                          Specialist (Gemma 2B)
```

**Design Patterns**: Agent Pattern, Orchestrator Pattern, Repository Pattern

## 💻 Tech Stack

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.14 |
| **AI Model** | Gemma 2B (Google) |
| **LLM Runtime** | Ollama |
| **Web UI** | Gradio |
| **Data Validation** | Pydantic |
| **Web Scraping** | BeautifulSoup, Feedparser |

## ⚡ Quick Start

```bash
# Install dependencies
./install_deps.sh

# Pull AI model
ollama pull gemma:2b

# Start Ollama (terminal 1)
ollama serve

# Launch application (terminal 2)
./run_app.sh
```

**Access:** http://localhost:7861

## 📊 Project Stats

- **Lines of Code**: ~550 (clean, modular)
- **Agents**: 5 specialized components
- **Processing Time**: 10-15s per discovery run
- **Memory Footprint**: ~2GB (includes model)

## 🎨 Code Highlights

### Multi-Agent Implementation
```python
class PlanningAgent(Agent):
    def plan(self, memory):
        selection = self.scanner.scan(memory)
        opportunities = [self._calculate_opportunity(d) 
                        for d in selection.deals]
        best = self._get_best_opportunity(opportunities)
        if self._should_alert(best.discount):
            self.messenger.alert(best)
        return best
```

### Local LLM Integration
```python
class SpecialistAgent(Agent):
    def price(self, description):
        prompt = self._create_prompt(description)
        response = self._call_ollama(prompt)
        return self._extract_number(response)
```

## 🔧 Configuration

**Threshold** (`agents/planning_agent.py`):
```python
DEAL_THRESHOLD = 0  # Minimum discount
```

**Model** (`agents/specialist_agent.py`):
```python
MODEL = "gemma:2b"
```

## 📂 Structure

```
├── agents/              # Agent implementations
│   ├── planning_agent.py
│   ├── scanner_agent.py
│   ├── specialist_agent.py
│   └── ...
├── app.py              # Gradio interface
├── deal_agent_framework.py
└── requirements.txt
```

## 🎓 Technical Skills Demonstrated

- **AI/ML**: LLM integration, prompt engineering, ensemble learning
- **Software Architecture**: Multi-agent systems, design patterns, modularity
- **Python**: Type hints, Pydantic, async patterns, OOP
- **Web Development**: Gradio, REST APIs, HTTP clients
- **Data Processing**: Web scraping, regex, JSON serialization
- **DevOps**: Shell scripting, dependency management, version control

## 📈 Performance

- **Scalability**: Modular design allows easy agent addition
- **Efficiency**: Local inference with optimized model
- **Reliability**: Error handling, fallback mechanisms, logging

## 🔒 Privacy & Security

- **100% Local Processing**: No data leaves your machine
- **No API Keys**: Self-contained system
- **Zero External Dependencies**: For core AI functionality

## 📚 Documentation

- **Technical Deep Dive**: `TECHNICAL_DOCUMENTATION.md`
- **Code Examples**: `example.py`

## 🛠️ Development

**Adding New Agents:**
```python
from agents.agent import Agent

class CustomAgent(Agent):
    name = "Custom Agent"
    def process(self, data):
        self.log("Processing")
        return result
```

## 🎯 Use Cases

- E-commerce price monitoring
- Deal aggregation platforms
- Market research tools
- Price comparison systems

## 📝 Key Learnings

1. Implemented hierarchical multi-agent system from scratch
2. Integrated local LLM (Gemma 2B) for production use
3. Designed modular architecture for scalability
4. Built responsive web interface with Gradio
5. Optimized for privacy with local-first approach

## 🔗 Connect

**Portfolio**: [Your Portfolio Link]  
**LinkedIn**: [Your LinkedIn]  
**Email**: [Your Email]

## 📄 License

MIT License - Open source and free to use.

---

**Built with**: Multi-Agent AI Architecture • Ollama • Gemma 2B • Python • Gradio

*Demonstrating practical AI engineering, clean code principles, and production-ready system design.*
