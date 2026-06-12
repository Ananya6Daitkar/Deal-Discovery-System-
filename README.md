# Multi-Agent Deal Discovery System

> Intelligent AI system that autonomously discovers deals, estimates prices using **Gemma 2B**, and identifies bargains through multi-agent orchestration.

## Overview

Production-ready hierarchical multi-agent system demonstrating modern AI architecture with dual deployment options: **local Ollama inference** and **Modal.com serverless deployment**.

**Key Achievement:** Implements Agent Pattern, Orchestrator Pattern, and ensemble learning with fine-tuned LLM for price estimation.

## Tech Stack

**Core**: Python 3.14 • Gemma 2B • Ollama • Gradio  
**ML/AI**: HuggingFace Transformers • PEFT • BitsAndBytes • 4-bit Quantization  
**Infrastructure**: Modal.com (Serverless GPU) • Local Inference  
**Data**: BeautifulSoup • Feedparser • Pydantic • JSON

## Architecture

```
Framework → Planning Agent → Scanner | Ensemble | Messaging
                                ↓
                     Specialist (Gemma 2B via Ollama/Modal)
```

**5 Specialized Agents:**
- **Scanner Agent**: RSS feed parsing, regex-based price extraction
- **Specialist Agent**: LLM-powered price estimation (local Ollama)
- **Ensemble Agent**: Aggregates multi-model predictions
- **Planning Agent**: Orchestrates workflow, calculates opportunities
- **Messaging Agent**: Formats alerts and notifications

## Deployment Options

### 1. Local Deployment (Ollama)
```bash
./install_deps.sh
ollama pull gemma:2b
ollama serve          # Terminal 1
./run_app.sh          # Terminal 2
```
**Access:** http://localhost:7861

### 2. Serverless Deployment (Modal.com)
`pricer_service.py` provides GPU-accelerated inference using:
- **Infrastructure as Code** with Modal
- **T4 GPU** serverless compute
- **Fine-tuned Gemma 2B** from HuggingFace
- **4-bit Quantization** (NF4) for efficiency
- **PEFT** for parameter-efficient fine-tuning

```python
@app.function(image=image, secrets=secrets, gpu=GPU, timeout=1800)
def price(description: str) -> float:
    # Loads fine-tuned model with quantization
    # Returns predicted price
```

**Deployment**:
```bash
modal deploy pricer_service.py
```

## Code Highlights

**Multi-Agent Orchestration:**
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

**Serverless Price Inference:**
```python
fine_tuned_model = PeftModel.from_pretrained(
    base_model, FINETUNED_MODEL, revision=REVISION
)
with torch.no_grad():
    outputs = fine_tuned_model.generate(inputs, max_new_tokens=5)
```

## Project Structure

```
├── agents/                    # Agent implementations
│   ├── planning_agent.py      # Orchestrator
│   ├── scanner_agent.py       # RSS + price extraction
│   ├── specialist_agent.py    # Ollama LLM integration
│   ├── ensemble_agent.py      # Model aggregation
│   └── messaging_agent.py     # Notification formatting
├── app.py                     # Gradio web interface
├── pricer_service.py          # Modal serverless deployment
├── deal_agent_framework.py    # Core framework
└── TECHNICAL_DOCUMENTATION.md # Full technical specs
```

## Technical Skills Demonstrated

**AI/ML Engineering:**
- Multi-agent systems architecture
- LLM fine-tuning with PEFT/LoRA
- 4-bit quantization for efficiency
- Prompt engineering and inference optimization
- Ensemble learning techniques

**Software Engineering:**
- Design patterns (Agent, Orchestrator, Repository)
- Type-safe Python with Pydantic
- Modular, maintainable architecture
- Error handling and logging

**Infrastructure:**
- Serverless GPU deployment (Modal.com)
- Local LLM deployment (Ollama)
- Infrastructure as code
- Web scraping and data pipelines

**Full Stack:**
- Gradio web interface
- REST API design
- JSON persistence
- Shell scripting

## Key Features

- **100% Privacy-Focused**: Local processing, no cloud APIs required
- **Dual Deployment**: Choose serverless (Modal) or local (Ollama)
- **Production Ready**: Error handling, logging, persistent memory
- **Scalable**: Modular design for easy agent extension
- **Efficient**: ~550 LOC, 10-15s processing time

## Configuration

Adjust thresholds in `agents/planning_agent.py`:
```python
DEAL_THRESHOLD = 0  # Minimum discount percentage
```

Switch models in `agents/specialist_agent.py`:
```python
MODEL = "gemma:2b"  # Any Ollama-compatible model
```

---

**Built with**: Multi-Agent AI • Gemma 2B • Modal.com • Ollama • Python • Gradio

*Demonstrating production-ready AI engineering, serverless infrastructure, and clean architectural design.*
