"""Configuration file for feature toggles"""

# PRICING CONFIGURATION
# Enable Modal.com fallback for better accuracy (requires Modal deployment)
USE_MODAL_FALLBACK = False
MODAL_URL = "https://ed-donner--pricer-service-price.modal.run"

# RAG CONFIGURATION
# Enable RAG with vector store for context-aware pricing
USE_RAG = False  # Set to True to enable RAG functionality

# OLLAMA CONFIGURATION
OLLAMA_MODEL = "gemma:2b"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"  # For RAG embeddings

# RSS FEED CONFIGURATION
# Demo data is automatically used as fallback when RSS feeds fail
USE_DEMO_DATA_FALLBACK = True

# DEAL THRESHOLD
DEAL_THRESHOLD = 0  # Minimum discount percentage to alert

# WEB UI
GRADIO_PORT = 7861
