# Quick Start Guide

Get the Local Agentic AI System up and running in minutes.

## Prerequisites

- Python 3.10 or higher
- pip package manager

## Installation

1. **Install dependencies**:
```bash
pip install pydantic pydantic-settings pyyaml rich python-dotenv
```

2. **Set up configuration** (choose one):

   **Option A: Environment Variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your settings
   # (defaults work fine for local development)
   ```

   **Option B: YAML Configuration**
   ```bash
   # Copy the example file
   cp config.yaml.example config.yaml
   
   # Edit config.yaml with your settings
   ```

## Verify Installation

Run the test suite:
```bash
python test_config_logging.py
```

Expected output:
```
============================================================
Configuration and Logging Test Suite
============================================================

=== Test 1: Default Configuration ===
✓ LLM Provider: ollama
✓ LLM Model: llama3
...

============================================================
✓ All tests passed successfully!
============================================================
```

## Try the Demo

Run the interactive demo:
```bash
python demo_config_logging.py
```

This demonstrates:
- Configuration loading
- Structured logging
- Request ID tracking
- Error handling with tracebacks

## Basic Usage

### 1. Load Configuration

```python
from app.config import get_config

# Load configuration
config = get_config()

# Access settings
print(f"Using {config.llm.provider} with model {config.llm.model_name}")
print(f"API will run on {config.api.host}:{config.api.port}")
```

### 2. Use Logging

```python
from app.logger import get_logger

# Create a logger
logger = get_logger(__name__)

# Log messages
logger.info("Application started")
logger.warning("This is a warning")
logger.error("This is an error")
```

### 3. Track Requests

```python
from app.logger import get_logger, log_with_context

logger = get_logger(__name__)

# Log with request ID and context
log_with_context(
    logger,
    "info",
    "Processing user request",
    request_id="req-12345",
    user_id="user-789",
    action="query"
)
```

## Configuration Options

### Change Log Level

**Via Environment Variable**:
```bash
export LOG_LEVEL=DEBUG
python demo_config_logging.py
```

**Via Code**:
```python
from app.logger import configure_logging

configure_logging(level="DEBUG")
```

### Change LLM Provider

**Via Environment Variable**:
```bash
export LLM_PROVIDER=huggingface
export LLM_MODEL_NAME=meta-llama/Llama-3-8B
```

**Via YAML** (`config.yaml`):
```yaml
llm:
  provider: huggingface
  model_name: meta-llama/Llama-3-8B
```

### Change API Port

**Via Environment Variable**:
```bash
export API_PORT=8080
```

**Via YAML** (`config.yaml`):
```yaml
api:
  port: 8080
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pydantic_settings'"

**Solution**: Install the missing dependency
```bash
pip install pydantic-settings
```

### Issue: Configuration not loading from .env file

**Solution**: Ensure `.env` file is in the project root directory
```bash
# Check if .env exists
ls -la .env

# If not, copy from example
cp .env.example .env
```

### Issue: Logs not showing up

**Solution**: Check log level configuration
```python
from app.logger import configure_logging

# Set to DEBUG to see all logs
configure_logging(level="DEBUG")
```

## Next Steps

1. **Implement LLM Client** (Task 2)
   - Connect to Ollama or HuggingFace
   - Add retry logic with exponential backoff

2. **Implement RAG Engine** (Task 3)
   - Set up ChromaDB vector store
   - Implement document chunking and embedding

3. **Build LangGraph State Machine** (Task 5)
   - Define agent workflow states
   - Implement research-to-summary workflow

4. **Create FastAPI Endpoints** (Task 7)
   - Expose workflow execution endpoint
   - Add document management endpoints

## Resources

- **README.md** - Full project documentation
- **IMPLEMENTATION_STATUS.md** - Current implementation status
- **test_config_logging.py** - Comprehensive test suite
- **demo_config_logging.py** - Interactive demo
- **.env.example** - Environment variable template
- **config.yaml.example** - YAML configuration template

## Support

For issues or questions:
1. Check the test suite: `python test_config_logging.py`
2. Review the demo: `python demo_config_logging.py`
3. Read the full documentation in README.md
4. Check IMPLEMENTATION_STATUS.md for current progress

## What's Working Now

✅ Configuration management (environment variables + YAML)  
✅ Centralized logging with Rich console output  
✅ Request ID tracking  
✅ Structured logging with context data  
✅ Error logging with tracebacks  
✅ Configurable log levels  
✅ JSON format for production  

## What's Coming Next

🚧 Local LLM client with retry logic  
🚧 RAG engine with ChromaDB  
🚧 LangGraph state machine  
🚧 FastAPI endpoints  
🚧 Initialization script  
🚧 Property-based tests  

---

**Ready to build?** Start with Task 2: Implement Local LLM Client!
