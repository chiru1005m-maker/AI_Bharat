# Local Agentic AI System

A privacy-focused, local-first agent framework combining stateful workflow management with retrieval-augmented generation (RAG).

## Architecture

- **API Layer**: FastAPI application with HTTP endpoints
- **Agent Layer**: LangGraph-based state machine for workflow execution
- **Storage Layer**: ChromaDB vector store for document embeddings
- **LLM Integration**: Local models via Ollama/Llama 3 or HuggingFace

## Project Structure

```
.
├── app/                    # API layer and core utilities
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── logger.py          # Centralized logging
│   └── main.py            # FastAPI application (TBD)
├── agents/                 # Agent workflow logic
│   ├── __init__.py
│   ├── graph.py           # LangGraph state machine (TBD)
│   └── llm_client.py      # Local LLM client (TBD)
├── db/                     # Database and RAG engine
│   ├── __init__.py
│   └── rag.py             # RAG engine with ChromaDB (TBD)
├── schemas/                # Pydantic models
│   └── __init__.py
├── tests/                  # Test suite
│   ├── unit/
│   ├── property/
│   └── integration/
├── .env.example           # Environment variable template
├── config.yaml.example    # YAML configuration template
└── test_config_logging.py # Configuration and logging tests
```

## Configuration

The system supports two configuration methods:

### 1. Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
# LLM Configuration
LLM_PROVIDER=ollama
LLM_MODEL_NAME=llama3
LLM_EMBEDDING_MODEL=nomic-embed-text
LLM_BASE_URL=http://localhost:11434

# Vector Store Configuration
VECTOR_PERSIST_DIRECTORY=./chroma_db
VECTOR_CHUNK_SIZE=512

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Logging Configuration
LOG_LEVEL=INFO
LOG_JSON_FORMAT=false
```

### 2. YAML Configuration

Copy `config.yaml.example` to `config.yaml` and customize:

```yaml
llm:
  provider: ollama
  model_name: llama3
  embedding_model: nomic-embed-text
  base_url: http://localhost:11434

vector_store:
  persist_directory: ./chroma_db
  chunk_size: 512

api:
  host: 0.0.0.0
  port: 8000

log:
  level: INFO
  json_format: false
```

### Loading Configuration

```python
from app.config import get_config

# Load from environment variables (default)
config = get_config()

# Load from YAML file
config = get_config(yaml_path="config.yaml")

# Access configuration
print(config.llm.model_name)
print(config.api.port)
```

## Logging

The system uses a centralized logging module with rich console output.

### Basic Usage

```python
from app.logger import get_logger

logger = get_logger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Request ID Tracking

```python
from app.logger import get_logger

# Create logger with request ID
logger = get_logger(__name__, request_id="req-12345")
logger.info("Processing request")
```

### Structured Logging

```python
from app.logger import log_with_context

log_with_context(
    logger,
    "info",
    "API request received",
    request_id="req-001",
    endpoint="/workflow/research-summary",
    method="POST",
    latency_ms=125.5
)
```

### Configure Log Level

```python
from app.logger import configure_logging

# Set log level globally
configure_logging(level="DEBUG")

# Enable JSON format for production
configure_logging(level="INFO", json_format=True)
```

## Testing

Run the configuration and logging tests:

```bash
python test_config_logging.py
```

This verifies:
- ✓ Configuration loads from environment variables
- ✓ Environment variables override defaults
- ✓ Logger respects configured log levels
- ✓ Request ID tracking works
- ✓ Structured logging with extra data
- ✓ Error logging with exception tracebacks

## Development Status

### Completed ✓
- [x] Project structure setup
- [x] Configuration management (Pydantic BaseSettings)
- [x] Centralized logging (Rich console output)
- [x] Environment variable support
- [x] YAML configuration support

### In Progress 🚧
- [ ] Local LLM client with retry logic
- [ ] RAG engine with ChromaDB
- [ ] LangGraph state machine
- [ ] FastAPI endpoints
- [ ] Initialization script

### Planned 📋
- [ ] Property-based tests
- [ ] Unit tests
- [ ] Integration tests
- [ ] Documentation

## Requirements

- Python 3.10+
- pydantic >= 2.0
- pydantic-settings
- rich
- pyyaml

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Copy configuration templates
cp .env.example .env
cp config.yaml.example config.yaml

# Run tests
python test_config_logging.py
```

## License

MIT
