"""
Quick Demo: Configuration and Logging System

Shows practical usage of the configuration and logging modules.
"""

from app.config import get_config
from app.logger import get_logger, log_with_context, configure_logging


def main():
    print("=" * 70)
    print("Local Agentic AI System - Configuration & Logging Demo")
    print("=" * 70)
    
    # Load configuration
    print("\n📋 Loading Configuration...")
    config = get_config()
    
    print(f"   LLM: {config.llm.provider} ({config.llm.model_name})")
    print(f"   Vector Store: {config.vector_store.persist_directory}")
    print(f"   API Server: {config.api.host}:{config.api.port}")
    print(f"   Log Level: {config.log.level}")
    
    # Configure logging
    configure_logging(level=config.log.level)
    
    # Create loggers for different components
    print("\n📝 Demonstrating Logging...")
    
    api_logger = get_logger("app.api")
    agent_logger = get_logger("agents.graph")
    rag_logger = get_logger("db.rag")
    
    # Simulate API request
    print("\n--- Simulating API Request ---")
    api_logger.info("Received POST request to /workflow/research-summary")
    log_with_context(
        api_logger,
        "info",
        "Request validated successfully",
        request_id="req-demo-001",
        endpoint="/workflow/research-summary",
        query="What is LangGraph?"
    )
    
    # Simulate agent workflow
    print("\n--- Simulating Agent Workflow ---")
    agent_logger.info("Initializing workflow state")
    log_with_context(
        agent_logger,
        "info",
        "State transition: START → RESEARCH",
        request_id="req-demo-001",
        from_node="start",
        to_node="research",
        step_count=1
    )
    
    # Simulate RAG query
    print("\n--- Simulating RAG Query ---")
    rag_logger.info("Querying vector store for relevant documents")
    log_with_context(
        rag_logger,
        "info",
        "Retrieved documents from ChromaDB",
        request_id="req-demo-001",
        query="What is LangGraph?",
        top_k=5,
        documents_found=3,
        query_time_ms=45.2
    )
    
    # Simulate synthesis
    print("\n--- Simulating Synthesis Phase ---")
    log_with_context(
        agent_logger,
        "info",
        "State transition: RESEARCH → SYNTHESIS",
        request_id="req-demo-001",
        from_node="research",
        to_node="synthesis",
        step_count=2
    )
    agent_logger.info("Combining retrieved documents into context")
    
    # Simulate summary generation
    print("\n--- Simulating Summary Generation ---")
    log_with_context(
        agent_logger,
        "info",
        "State transition: SYNTHESIS → SUMMARY",
        request_id="req-demo-001",
        from_node="synthesis",
        to_node="summary",
        step_count=3
    )
    agent_logger.info("Generating final summary using local LLM")
    
    # Simulate completion
    print("\n--- Workflow Complete ---")
    log_with_context(
        api_logger,
        "info",
        "Workflow completed successfully",
        request_id="req-demo-001",
        total_steps=3,
        execution_time_ms=1250.5,
        status="success"
    )
    
    # Simulate warning
    print("\n--- Simulating Warning ---")
    rag_logger.warning("Vector store approaching capacity (85% full)")
    
    # Simulate error handling
    print("\n--- Simulating Error Handling ---")
    try:
        # Simulate an error
        raise ConnectionError("Failed to connect to local LLM at http://localhost:11434")
    except ConnectionError as e:
        api_logger.error("LLM connection failed", exc_info=True)
        log_with_context(
            api_logger,
            "error",
            "Retrying LLM connection with exponential backoff",
            request_id="req-demo-002",
            error_type=type(e).__name__,
            retry_attempt=1,
            next_retry_in_seconds=2
        )
    
    print("\n" + "=" * 70)
    print("✓ Demo Complete!")
    print("=" * 70)
    print("\nTip: Set LOG_LEVEL=DEBUG to see more detailed logs")
    print("     Set LOG_JSON_FORMAT=true for production JSON logs")


if __name__ == "__main__":
    main()
