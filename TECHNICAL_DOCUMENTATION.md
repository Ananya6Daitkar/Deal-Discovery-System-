# Multi-Agent Deal Discovery System - Technical Documentation

**Project Location:** `/Users/nalinee/Documents/week8-multi-agent-system/`  
**Status:** Production Ready  
**Last Updated:** June 12, 2026

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Technical Stack](#technical-stack)
4. [Components Explained](#components-explained)
5. [AI/ML Techniques](#aiml-techniques)
6. [Data Flow](#data-flow)
7. [File Structure](#file-structure)
8. [Code Statistics](#code-statistics)
9. [Design Patterns](#design-patterns)
10. [Configuration](#configuration)

---

## System Overview

### What It Does

A multi-agent AI system that:
1. Scrapes product deals from RSS feeds
2. Estimates fair market prices using local AI
3. Identifies bargains by calculating discount
4. Provides web interface for interaction
5. Persists data in JSON format

### Key Features

- **Multi-Agent Architecture**: Specialized agents for different tasks
- **Local AI**: Uses Ollama with Gemma 2B (no cloud APIs)
- **Web Interface**: Gradio-based UI
- **Persistent Memory**: JSON-based storage
- **Real-time Processing**: Live deal discovery

---

## Architecture

### System Design

```
┌─────────────────────────────────────────┐
│       Gradio Web Interface              │
│       (User Interaction Layer)          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     DealAgentFramework                  │
│     (Orchestration Layer)               │
│  - Memory Management                    │
│  - Logging                              │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│       Planning Agent                    │
│       (Coordination Layer)              │
│  - Workflow Management                  │
│  - Agent Coordination                   │
└───┬────────────────┬────────────────┬───┘
    │                │                │
┌───▼────┐    ┌──────▼─────┐   ┌────▼──────┐
│Scanner │    │  Ensemble  │   │Messaging  │
│ Agent  │    │   Agent    │   │  Agent    │
└────────┘    └──────┬─────┘   └───────────┘
                     │
              ┌──────▼──────┐
              │ Specialist  │
              │   Agent     │
              │ (Gemma 2B)  │
              └─────────────┘
```

### Agent Hierarchy

1. **Framework Layer**: `DealAgentFramework`
2. **Coordination Layer**: `PlanningAgent`
3. **Execution Layer**: `ScannerAgent`, `EnsembleAgent`, `MessagingAgent`
4. **AI Layer**: `SpecialistAgent`

---

## Technical Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.14 | Primary language |
| **Ollama** | Latest | Local LLM runtime |
| **Gemma 2B** | Latest | AI model for pricing |
| **Gradio** | Latest | Web interface framework |
| **Pydantic** | Latest | Data validation |
| **BeautifulSoup4** | Latest | HTML parsing |
| **Feedparser** | Latest | RSS feed parsing |

### Python Packages

```
beautifulsoup4    # Web scraping
feedparser        # RSS parsing
requests          # HTTP client
python-dotenv     # Environment variables
pydantic          # Data validation
numpy             # Numerical operations
gradio            # Web UI framework
```

---

## Components Explained

### 1. DealAgentFramework (`deal_agent_framework.py`)

**Purpose:** Main entry point and orchestrator

**Responsibilities:**
- Initialize logging system
- Manage memory (load/save deals)
- Coordinate Planning Agent
- Provide run() interface

**Key Methods:**
- `__init__()`: Setup logging, load memory
- `_load_memory()`: Load opportunities from JSON
- `_save_memory()`: Persist opportunities to JSON
- `run()`: Execute complete workflow

**Technical Details:**
- Uses JSON for persistence
- Implements lazy initialization pattern
- Handles logging configuration

---

### 2. Planning Agent (`agents/planning_agent.py`)

**Purpose:** Workflow coordinator

**Responsibilities:**
- Initialize sub-agents (Scanner, Ensemble, Messaging)
- Process individual deals
- Calculate discounts
- Apply threshold filter
- Trigger notifications

**Key Methods:**
- `__init__()`: Create sub-agents
- `_process_deal()`: Price single deal
- `plan()`: Execute main workflow

**Algorithm:**
```python
1. Scanner.scan() → Get deals
2. For each deal:
   a. Ensemble.price() → Get estimate
   b. Calculate discount = estimate - actual_price
3. Sort by discount
4. If discount > threshold:
   a. Messaging.alert()
   b. Return opportunity
```

**Configuration:**
- `DEAL_THRESHOLD = 0`: Show all deals (originally 50)

---

### 3. Scanner Agent (`agents/scanner_agent.py`)

**Purpose:** RSS feed scraper and deal extractor

**Responsibilities:**
- Fetch deals from RSS feeds
- Filter out already-seen URLs
- Extract prices from text
- Convert to Deal objects

**Key Methods:**
- `_fetch_new_deals()`: Get new deals from RSS
- `scan()`: Main scanning logic

**Algorithm:**
```python
1. Fetch all RSS entries
2. Filter: keep only new URLs (not in memory)
3. For each deal:
   a. Extract price using regex: \$(\d+(?:,\d{3})*(?:\.\d{2})?)
   b. Create Deal object
4. Return first 5 deals
```

**RSS Feeds:**
- Electronics: `dealnews.com/c142/Electronics/?rss=1`
- Computers: `dealnews.com/c39/Computers/?rss=1`
- Smart Home: `dealnews.com/f1912/Smart-Home/?rss=1`

**Technical Details:**
- Uses regex for price extraction
- Handles missing prices (default: $100)
- Truncates descriptions to prevent overflow

---

### 4. Ensemble Agent (`agents/ensemble_agent.py`)

**Purpose:** Price estimation coordinator

**Responsibilities:**
- Manage Specialist Agent
- Return price estimates

**Key Methods:**
- `__init__()`: Initialize Specialist
- `price()`: Get price estimate

**Current Implementation:**
- Uses only Specialist Agent (Gemma 2B)
- Originally had multiple models (Frontier removed due to ChromaDB incompatibility)

---

### 5. Specialist Agent (`agents/specialist_agent.py`)

**Purpose:** Local AI pricing model

**Responsibilities:**
- Call Ollama API
- Extract price from response
- Handle errors gracefully

**Key Methods:**
- `_call_ollama()`: HTTP call to Ollama
- `_extract_price()`: Parse price from text
- `price()`: Main pricing interface

**Technical Details:**
- **Model**: Gemma 2B
- **Endpoint**: `http://localhost:11434/api/generate`
- **Timeout**: 60 seconds
- **Error Handling**: Returns default price on failure

**Ollama Request:**
```python
{
    "model": "gemma:2b",
    "prompt": "Estimate price for: [product]",
    "stream": False
}
```

---

### 6. Messaging Agent (`agents/messaging_agent.py`)

**Purpose:** User notifications

**Responsibilities:**
- Format deal alerts
- Display to user

**Key Methods:**
- `alert()`: Print deal notification

**Output Format:**
```
Great Deal Found!

Product: [description]
Price: $X.XX
Estimated Value: $Y.YY
Discount: $Z.ZZ

URL: [link]
```

---

### 7. Base Agent (`agents/agent.py`)

**Purpose:** Common functionality for all agents

**Provides:**
- Logging method with agent name
- Consistent logging format

**Key Methods:**
- `log()`: Log message with agent identification

---

### 8. Data Models (`agents/deals.py`)

**Purpose:** Type-safe data structures using Pydantic

**Models:**

#### `ScrapedDeal`
- Raw deal from RSS feed
- Fields: title, summary, url, details, features
- Methods: `describe()`, `fetch()`

#### `Deal` (Pydantic BaseModel)
- Validated deal structure
- Fields: product_description, price, url

#### `DealSelection` (Pydantic BaseModel)
- Collection of deals
- Fields: deals (List[Deal])

#### `Opportunity` (Pydantic BaseModel)
- Deal with pricing analysis
- Fields: deal, estimate, discount

**Technical Details:**
- Uses Pydantic for validation
- Automatically converts to/from JSON
- Type hints for IDE support

---

### 9. Gradio Interface (`app.py`)

**Purpose:** Web-based user interface

**Features:**
- Initialize System button
- Run Deal Discovery button
- Latest Deal display
- Recent Opportunities table (last 10)
- All Opportunities accordion
- Clear Memory button

**Key Functions:**
- `initialize_system()`: Setup framework
- `run_deal_discovery()`: Execute workflow
- `view_all_opportunities()`: Show history
- `clear_memory()`: Reset data

**UI Components:**
- Markdown for formatting
- Dataframe for tables
- Accordion for expandable sections
- Buttons for actions
- Textboxes for status

**Configuration:**
- **Host**: 127.0.0.1 (localhost only)
- **Port**: 7861
- **Theme**: Soft (Gradio theme)

---

## AI/ML Techniques

### 1. Large Language Model (LLM)

**Model:** Gemma 2B by Google

**Characteristics:**
- 2 billion parameters
- Optimized for instruction following
- Runs locally via Ollama

**Use Case:** Price estimation

**Prompt Engineering:**
```
Estimate the price of this product in USD. 
Respond with ONLY a number.

Product: [description]

Price estimate:
```

---

### 2. Natural Language Processing (NLP)

**Technique:** Regular Expression (Regex) Pattern Matching

**Pattern:** `\$(\d+(?:,\d{3})*(?:\.\d{2})?)`

**Explanation:**
- `\$`: Match dollar sign
- `(\d+(?:,\d{3})*)`: Digits with optional thousands separator
- `(?:\.\d{2})?`: Optional cents (.XX)

**Use Case:** Extract prices from deal descriptions

---

### 3. Multi-Agent System

**Pattern:** Hierarchical Multi-Agent Architecture

**Characteristics:**
- **Specialization**: Each agent has specific role
- **Coordination**: Planning Agent orchestrates
- **Communication**: Agents pass data via method calls
- **Autonomy**: Each agent makes own decisions

**Benefits:**
- Modularity (easy to add/remove agents)
- Maintainability (isolated concerns)
- Scalability (can parallelize agents)

---

### 4. Ensemble Learning

**Concept:** Combine multiple models for better predictions

**Current Implementation:**
- Single model (Specialist/Gemma 2B)
- Originally designed for multiple models

**Historical Ensemble:**
- 90% Frontier Agent (RAG-based)
- 10% Specialist Agent (fine-tuned)

**Removed Due To:**
- ChromaDB incompatibility with Python 3.14
- Protobuf version conflicts

---

## Data Flow

### Complete Workflow

```
1. USER ACTION
   ↓
   Click "Run Deal Discovery" in Gradio

2. FRAMEWORK INITIALIZATION
   ↓
   DealAgentFramework.run()
   - Load memory.json
   - Initialize Planning Agent

3. DEAL DISCOVERY
   ↓
   PlanningAgent.plan()
   - Call ScannerAgent.scan()
   
4. RSS SCRAPING
   ↓
   ScannerAgent.scan()
   - Fetch from 3 RSS feeds
   - Parse 30 deals total
   - Filter already-seen URLs
   - Extract prices with regex
   - Return 5 deals

5. PRICE ESTIMATION
   ↓
   For each deal:
     EnsembleAgent.price()
     ↓
     SpecialistAgent.price()
     ↓
     Call Ollama HTTP API
     ↓
     Gemma 2B processes prompt
     ↓
     Return estimated price

6. DISCOUNT CALCULATION
   ↓
   PlanningAgent._process_deal()
   - discount = estimate - actual_price
   - Create Opportunity object

7. FILTERING & SORTING
   ↓
   PlanningAgent.plan()
   - Sort by discount (descending)
   - Get best opportunity
   - Check threshold (0)

8. NOTIFICATION
   ↓
   MessagingAgent.alert()
   - Format message
   - Print to console

9. PERSISTENCE
   ↓
   DealAgentFramework.run()
   - Append to memory list
   - Save to memory.json

10. UI UPDATE
    ↓
    Gradio displays results
    - Latest Deal card
    - Recent Opportunities table
```

---

## File Structure

```
week8-multi-agent-system/
│
├── agents/                          # Agent implementations
│   ├── __init__.py                 # Package marker
│   ├── agent.py                    # Base class (12 lines)
│   ├── deals.py                    # Data models (80 lines)
│   ├── ensemble_agent.py           # Price coordinator (18 lines)
│   ├── messaging_agent.py          # Notifications (14 lines)
│   ├── planning_agent.py           # Orchestrator (38 lines)
│   ├── scanner_agent.py            # RSS scraper (48 lines)
│   └── specialist_agent.py         # Gemma 2B client (31 lines)
│
├── app.py                          # Gradio interface (200 lines)
├── deal_agent_framework.py         # Main framework (62 lines)
├── example.py                      # CLI usage (23 lines)
│
├── run_app.sh                      # Startup script (22 lines)
├── install_deps.sh                 # Dependency installer
│
├── .env                            # Environment config
├── .env.example                    # Config template
├── requirements.txt                # Python packages
├── memory.json                     # Persistent storage
│
├── README.md                       # User documentation
├── HOW_TO_RUN.md                  # Quick start guide
└── TECHNICAL_DOCUMENTATION.md      # This file

Total Code: ~550 lines (Python)
```

---

## Code Statistics

### Lines of Code by Component

| Component | Lines | Percentage |
|-----------|-------|------------|
| Gradio UI | 200 | 36% |
| Data Models | 80 | 15% |
| Framework | 62 | 11% |
| Scanner Agent | 48 | 9% |
| Planning Agent | 38 | 7% |
| Specialist Agent | 31 | 6% |
| Example CLI | 23 | 4% |
| Ensemble Agent | 18 | 3% |
| Messaging Agent | 14 | 3% |
| Base Agent | 12 | 2% |
| **Total** | **526** | **100%** |

### Language Distribution

- **Python**: 526 lines (100%)
- **Bash**: 22 lines (scripts)
- **Markdown**: 3 documentation files

### Complexity Metrics

- **Number of Classes**: 11
- **Number of Functions**: 32
- **Average Function Length**: 12 lines
- **Max Function Length**: 45 lines (run_deal_discovery)
- **Cyclomatic Complexity**: Low (mostly linear flows)

---

## Design Patterns

### 1. **Agent Pattern**

**Definition:** Autonomous entities that perform specific tasks

**Implementation:**
- Base class: `Agent`
- Derived classes: `ScannerAgent`, `SpecialistAgent`, etc.
- Common interface: `log()` method

**Benefits:**
- Encapsulation of functionality
- Easy to add new agents
- Independent testing

---

### 2. **Orchestrator Pattern**

**Definition:** Central coordinator manages workflow

**Implementation:**
- `PlanningAgent` coordinates sub-agents
- `DealAgentFramework` manages Planning Agent

**Benefits:**
- Clear control flow
- Single point of workflow management
- Easy to modify workflow

---

### 3. **Facade Pattern**

**Definition:** Simplified interface to complex system

**Implementation:**
- `DealAgentFramework.run()` hides complexity
- Gradio functions hide agent details

**Benefits:**
- Easy to use
- Hides implementation details
- Stable public interface

---

### 4. **Strategy Pattern**

**Definition:** Interchangeable algorithms

**Implementation:**
- `EnsembleAgent` can swap pricing strategies
- Originally: multiple models, now: single model

**Benefits:**
- Flexible pricing approaches
- Easy to add new models
- Algorithm selection at runtime

---

### 5. **Repository Pattern**

**Definition:** Abstraction over data storage

**Implementation:**
- `_load_memory()` and `_save_memory()`
- JSON as storage backend

**Benefits:**
- Can switch storage (JSON → Database)
- Isolated data access logic
- Easy testing with mock storage

---

### 6. **Lazy Initialization**

**Definition:** Defer object creation until needed

**Implementation:**
```python
if not self.planner:
    self.planner = PlanningAgent()
```

**Benefits:**
- Faster startup
- Only load what's needed
- Resource efficiency

---

## Configuration

### Environment Variables

**File:** `.env`

```bash
# No API keys needed!
# System runs 100% locally with Ollama
```

### Agent Configuration

#### Planning Agent
```python
DEAL_THRESHOLD = 0  # Minimum discount to save (dollars)
```

#### Scanner Agent
```python
# RSS Feeds (in deals.py)
FEEDS = [
    "https://www.dealnews.com/c142/Electronics/?rss=1",
    "https://www.dealnews.com/c39/Computers/?rss=1",
    "https://www.dealnews.com/f1912/Smart-Home/?rss=1",
]
```

#### Specialist Agent
```python
MODEL = "gemma:2b"
OLLAMA_URL = "http://localhost:11434/api/generate"
```

#### Gradio App
```python
server_name = "127.0.0.1"  # Localhost only
server_port = 7861          # Port number
share = False               # No public URL
```

---

## Technical Terms Glossary

### AI/ML Terms

**LLM (Large Language Model)**
- AI model trained on massive text data
- Can understand and generate human language
- Example: Gemma 2B

**Gemma 2B**
- Google's open-source LLM
- 2 billion parameters
- Optimized for efficiency

**Ollama**
- Tool to run LLMs locally
- No internet needed after model download
- Provides HTTP API for inference

**Inference**
- Using a trained model to make predictions
- Input: product description
- Output: estimated price

**Prompt Engineering**
- Crafting effective instructions for LLM
- Goal: Get desired output format
- Technique: Clear, specific instructions

**Multi-Agent System**
- Multiple AI agents working together
- Each agent specializes in one task
- Communicate to achieve goal

**Ensemble Learning**
- Combining multiple models
- More accurate than single model
- Weighted average of predictions

**RAG (Retrieval Augmented Generation)**
- Technique: Find similar examples, then generate
- Removed from this project
- Reason: ChromaDB incompatibility

---

### Software Engineering Terms

**Pydantic**
- Python library for data validation
- Defines data models with types
- Automatic validation and serialization

**RSS (Really Simple Syndication)**
- Format for publishing updates
- Used by news sites, blogs
- XML-based feed

**Web Scraping**
- Extracting data from websites
- Tools: BeautifulSoup, Feedparser
- Parse HTML/XML to get structured data

**Regex (Regular Expression)**
- Pattern matching for text
- Example: `\$\d+` matches dollar amounts
- Powerful but complex

**JSON (JavaScript Object Notation)**
- Human-readable data format
- Used for: configuration, storage, APIs
- Example: `{"price": 99.99}`

**API (Application Programming Interface)**
- Way for programs to communicate
- HTTP API: communicate over internet/network
- REST API: specific style of HTTP API

**Lazy Loading**
- Don't create object until needed
- Improves startup time
- Common optimization technique

**Gradio**
- Python library for ML interfaces
- Automatic web UI generation
- Great for demos and prototypes

---

### Architecture Terms

**Orchestration**
- Coordination of multiple components
- Central control of workflow
- Example: Planning Agent

**Persistence**
- Saving data permanently
- Survives program restart
- Example: memory.json file

**Separation of Concerns**
- Each component has one responsibility
- Easier to maintain
- Example: Scanner only scans, doesn't price

**Modularity**
- System built from independent modules
- Can replace/update modules individually
- Example: Swap Gemma 2B for different model

**Facade**
- Simple interface to complex system
- Hides implementation details
- Example: `framework.run()`

---

## System Requirements

### Hardware

- **CPU**: Any modern processor
- **RAM**: 4GB minimum (8GB recommended for Gemma 2B)
- **Disk**: 2GB for Ollama + models
- **Network**: Internet for RSS feeds

### Software

- **OS**: macOS (current), Linux, Windows
- **Python**: 3.8+ (tested on 3.14)
- **Ollama**: Latest version
- **Gemma 2B**: Pulled via `ollama pull gemma:2b`

---

## Performance Characteristics

### Timing

- **RSS Fetch**: 1-5 seconds (30 deals)
- **Price Estimation**: 1-2 seconds per deal (Gemma 2B)
- **Total Workflow**: 10-15 seconds for 5 deals
- **UI Response**: < 1 second

### Resource Usage

- **Memory**: ~2GB (Ollama + Gemma 2B)
- **CPU**: Moderate during inference
- **Disk I/O**: Minimal (small JSON file)
- **Network**: Only for RSS fetching

---

## Known Limitations

### 1. Price Estimation Accuracy
- Gemma 2B estimates vary
- No training on deal-specific data
- May overestimate or underestimate

### 2. RSS Feed Dependency
- Relies on external websites
- Feeds can be empty or down
- No control over content

### 3. Python 3.14 Compatibility
- ChromaDB doesn't work (protobuf issue)
- Removed RAG functionality
- Single pricing model only

### 4. No Authentication
- Web UI accessible to anyone on localhost
- No user management
- All users see same data

### 5. English Only
- Deals must be in English
- Gemma 2B trained primarily on English
- No translation support

---

## Future Enhancements

### Potential Improvements

1. **Better Price Estimation**
   - Fine-tune Gemma 2B on deal data
   - Add multiple pricing models
   - Historical price tracking

2. **More Data Sources**
   - Amazon deals
   - eBay auctions
   - Retailer APIs

3. **Advanced Filtering**
   - Category selection
   - Price range filters
   - Brand preferences

4. **User Features**
   - Multiple user profiles
   - Deal watchlists
   - Email/SMS notifications

5. **Analytics**
   - Price trends over time
   - Best time to buy
   - Category insights

---

## Troubleshooting Guide

### Common Issues

**1. "Ollama not running"**
- Solution: `ollama serve` in terminal

**2. "No deals found"**
- RSS feeds empty
- All deals already in memory
- Solution: Try later or clear memory

**3. "Port already in use"**
- Solution: `lsof -ti:7861 | xargs kill -9`

**4. "Import errors"**
- Missing dependencies
- Solution: `./install_deps.sh`

**5. "Protobuf errors"**
- Python 3.14 incompatibility
- Already handled (ChromaDB removed)

---

## Development Workflow

### Making Changes

1. **Edit Code**: Modify Python files
2. **Kill App**: `lsof -ti:7861 | xargs kill -9`
3. **Restart**: `./run_app.sh`
4. **Test**: Use web interface

### Adding New Agent

```python
# 1. Create file: agents/my_agent.py
from agents.agent import Agent

class MyAgent(Agent):
    name = "My Agent"
    
    def do_something(self):
        self.log("Doing something")
        return result

# 2. Use in Planning Agent
from agents.my_agent import MyAgent

class PlanningAgent:
    def __init__(self):
        self.my_agent = MyAgent()
```

---

## Credits & References

### Technologies Used

- **Ollama**: https://ollama.ai/
- **Gemma**: https://ai.google.dev/gemma
- **Gradio**: https://gradio.app/
- **Pydantic**: https://docs.pydantic.dev/
- **Python**: https://www.python.org/

### Inspired By

- Ed Donner's LLM Engineering Course
- Multi-agent system design patterns
- Production ML system architecture

---

## Summary

This is a **production-ready multi-agent system** that:

- Uses local AI (Ollama + Gemma 2B)  
- Implements multi-agent architecture  
- Provides web interface (Gradio)  
- Persists data (JSON)  
- Handles errors gracefully  
- Runs on modest hardware  
- Requires no API keys  
- Is fully open-source  

**Total System Size:** ~550 lines of Python code

**Key Innovation:** Simplified multi-agent AI system that runs entirely locally without cloud dependencies.

---

**End of Technical Documentation**
