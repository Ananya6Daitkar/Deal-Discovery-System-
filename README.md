# Multi-Agent Deal Discovery System

An intelligent system that autonomously discovers product deals, estimates fair market prices, and identifies bargains using local AI.

## Overview

This system implements a multi-agent architecture where specialized AI agents collaborate to:
- Scan RSS feeds for product deals
- Estimate fair market prices using Gemma 2B
- Calculate potential discounts
- Alert users about opportunities


## Quick Start

### Prerequisites

- Python 3.8 or higher
- Ollama installed and running
- 4GB RAM minimum

### Installation

```bash
# 1. Clone or navigate to project directory
cd /Users/nalinee/Documents/week8-multi-agent-system

# 2. Install dependencies
./install_deps.sh

# 3. Pull AI model
ollama pull gemma:2b

# 4. Start Ollama (in separate terminal)
ollama serve

# 5. Launch application
./run_app.sh
```

### Access

Open your browser to: **http://localhost:7861**

## System Architecture

### Multi-Agent Design

The system employs a hierarchical multi-agent architecture:

```
Framework Layer (Orchestration)
    ↓
Planning Agent (Coordination)
    ↓
├─ Scanner Agent (Data Collection)
├─ Ensemble Agent (Price Estimation)
└─ Messaging Agent (Notifications)
    ↓
Specialist Agent (AI Model - Gemma 2B)
```

### Agent Responsibilities

| Agent | Purpose | Technology |
|-------|---------|------------|
| **Planning** | Workflow coordination | Python |
| **Scanner** | RSS feed scraping | BeautifulSoup |
| **Ensemble** | Price coordination | Python |
| **Specialist** | Price estimation | Ollama + Gemma 2B |
| **Messaging** | User notifications | Console output |

## Features

### Core Capabilities

- **Autonomous Operation**: Runs complete discovery workflow with one click
- **Local AI Processing**: No external API calls required
- **Persistent Memory**: Tracks previously discovered deals
- **Web Interface**: Modern Gradio-based UI
- **Real-time Processing**: Live deal analysis and pricing

### Technical Highlights

- Multi-agent system architecture
- Local LLM inference (Gemma 2B)
- RSS feed integration
- Pattern-based price extraction
- JSON-based data persistence
- Responsive web interface

## Usage

### Web Interface

1. **Initialize**: Click "Initialize System" (first time only)
2. **Discover**: Click "Run Deal Discovery"
3. **View**: See results in "Latest Deal" section
4. **History**: Expand "All Opportunities" for complete history
5. **Reset**: Use "Clear Memory" to start fresh

### Expected Behavior

- **Processing Time**: 10-15 seconds per discovery run
- **Deals Per Run**: Up to 5 deals analyzed
- **Memory**: Stores all discovered opportunities
- **Threshold**: Shows deals with any positive discount

### No Results?

If no deals appear:
- RSS feeds may be temporarily empty
- All current deals already discovered
- Feed sources might be updating

**Solution**: Try again in a few hours or clear memory to rediscover deals.

## Configuration

### System Settings

**Deal Threshold** (`agents/planning_agent.py`):
```python
DEAL_THRESHOLD = 0  # Minimum discount in dollars
```

**RSS Feeds** (`agents/deals.py`):
```python
FEEDS = [
    "https://www.dealnews.com/c142/Electronics/?rss=1",
    "https://www.dealnews.com/c39/Computers/?rss=1",
    "https://www.dealnews.com/f1912/Smart-Home/?rss=1",
]
```

**Ollama Model** (`agents/specialist_agent.py`):
```python
MODEL = "gemma:2b"
OLLAMA_URL = "http://localhost:11434/api/generate"
```

## Project Structure

```
week8-multi-agent-system/
├── agents/                  # Agent implementations
│   ├── agent.py            # Base agent class
│   ├── deals.py            # Data models
│   ├── ensemble_agent.py   # Price coordinator
│   ├── messaging_agent.py  # Notifications
│   ├── planning_agent.py   # Workflow orchestrator
│   ├── scanner_agent.py    # RSS scraper
│   └── specialist_agent.py # AI pricing model
│
├── app.py                  # Gradio web interface
├── deal_agent_framework.py # Main framework
├── example.py              # CLI usage example
│
├── run_app.sh             # Application launcher
├── install_deps.sh        # Dependency installer
│
├── memory.json            # Persistent storage
├── requirements.txt       # Python dependencies
│
├── README.md              # This file
├── HOW_TO_RUN.md         # Quick start guide
└── TECHNICAL_DOCUMENTATION.md  # Complete technical reference
```

## Technology Stack

### Core Technologies

- **Python 3.14**: Primary development language
- **Ollama**: Local LLM runtime environment
- **Gemma 2B**: Google's efficient language model
- **Gradio**: Web interface framework
- **Pydantic**: Data validation and serialization
- **BeautifulSoup**: HTML/XML parsing
- **Feedparser**: RSS feed processing

### Key Libraries

```
beautifulsoup4    - Web scraping
feedparser        - RSS parsing
requests          - HTTP client
python-dotenv     - Environment management
pydantic          - Data validation
numpy             - Numerical operations
gradio            - Web UI framework
```

## Development

### Adding New Features

The modular architecture allows easy extension:

**Add New Agent:**
```python
from agents.agent import Agent

class CustomAgent(Agent):
    name = "Custom Agent"
    
    def process(self, data):
        self.log("Processing data")
        return result
```

**Add New RSS Feed:**
```python
# Edit agents/deals.py
FEEDS = [
    "existing_feed_url",
    "new_feed_url",  # Add here
]
```

### Testing

```bash
# Test scanner agent
python3 test_scanner.py

# Test complete workflow
python3 example.py
```

## Troubleshooting

### Common Issues

**Ollama Not Running**
```bash
# Start Ollama service
ollama serve
```

**Port Already in Use**
```bash
# Kill existing process
lsof -ti:7861 | xargs kill -9
./run_app.sh
```

**Missing Model**
```bash
# Pull Gemma 2B model
ollama pull gemma:2b
```

**No Deals Found**
- Normal behavior - RSS feeds update periodically
- Check `memory.json` for previously discovered deals
- Try again later or clear memory

### Logs

Monitor terminal output for detailed execution logs:
```
[HH:MM:SS] [Agent Name] Message
```

## Performance

### Metrics

- **Startup Time**: < 2 seconds
- **Discovery Time**: 10-15 seconds
- **Memory Usage**: ~2GB (includes Ollama + model)
- **Disk Usage**: ~2GB (Ollama + models)
- **CPU Usage**: Moderate during AI inference

### Scalability

- Processes 5 deals per run
- Handles 30+ RSS entries
- Memory grows linearly with discovered deals
- No external rate limits

## Limitations

### Current Constraints

1. **Price Accuracy**: Estimates vary based on model training
2. **English Only**: Designed for English-language deals
3. **RSS Dependency**: Requires external feed availability
4. **Local Only**: No remote access configured
5. **Single User**: No multi-user support

### Known Issues

- ChromaDB removed due to Python 3.14 compatibility
- Protobuf version conflicts resolved
- Single pricing model (originally designed for ensemble)

## Security

### Data Privacy

- All processing occurs locally
- No data sent to external services
- No API keys required
- No user tracking or analytics

### Network Usage

- Outbound: RSS feed requests only
- Inbound: None (localhost only)
- No cloud service dependencies

## License

MIT License - Open source and freely modifiable.

## Credits

### Technologies

- **Ollama**: Local LLM runtime
- **Google Gemma**: Open-source language model
- **Gradio**: ML interface framework

### Inspiration

Based on multi-agent system design patterns and modern LLM application architecture.

## Support

### Documentation

- **Technical Details**: See `TECHNICAL_DOCUMENTATION.md`
- **Code Examples**: See `example.py`

### Resources

- Ollama Documentation: https://ollama.ai/
- Gemma Model: https://ai.google.dev/gemma
- Gradio Guide: https://gradio.app/

## Version History

### Current Version
- **Status**: Production Ready
- **Date**: June 12, 2026
- **Python**: 3.14
- **Model**: Gemma 2B
- **Code**: ~550 lines

### Recent Changes
- Simplified codebase (40% reduction)
- Removed ChromaDB (compatibility)
- Changed to Gemma 2B model
- Added comprehensive documentation
- Improved error handling

## Contact

For technical inquiries, refer to `TECHNICAL_DOCUMENTATION.md` for complete system specifications and architecture details.

---

**Built with modern multi-agent AI architecture for local, privacy-focused deal discovery.**
