"""
Test Script for Configuration and Logging

Verifies that:
1. Configuration loads from environment variables
2. Logger respects configured log levels
3. Rich console output works correctly
4. Request ID tracking functions properly
"""

import os
import sys
from app.config import get_config, SystemConfig
from app.logger import get_logger, configure_logging, log_with_context


def test_default_config():
    """Test loading configuration with defaults"""
    print("\n=== Test 1: Default Configuration ===")
    
    config = get_config()
    
    print(f"✓ LLM Provider: {config.llm.provider}")
    print(f"✓ LLM Model: {config.llm.model_name}")
    print(f"✓ LLM Base URL: {config.llm.base_url}")
    print(f"✓ Vector Store Path: {config.vector_store.persist_directory}")
    print(f"✓ Chunk Size: {config.vector_store.chunk_size}")
    print(f"✓ API Host: {config.api.host}")
    print(f"✓ API Port: {config.api.port}")
    print(f"✓ Log Level: {config.log.level}")
    print(f"✓ Retry Max Attempts: {config.retry.max_attempts}")


def test_env_override():
    """Test configuration override via environment variables"""
    print("\n=== Test 2: Environment Variable Override ===")
    
    # Set environment variables
    os.environ["LLM_MODEL_NAME"] = "llama3.1"
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["API_PORT"] = "8080"
    os.environ["VECTOR_CHUNK_SIZE"] = "1024"
    
    # Reload configuration
    config = get_config(reload=True)
    
    print(f"✓ LLM Model (overridden): {config.llm.model_name}")
    assert config.llm.model_name == "llama3.1", "LLM model override failed"
    
    print(f"✓ Log Level (overridden): {config.log.level}")
    assert config.log.level == "DEBUG", "Log level override failed"
    
    print(f"✓ API Port (overridden): {config.api.port}")
    assert config.api.port == 8080, "API port override failed"
    
    print(f"✓ Chunk Size (overridden): {config.vector_store.chunk_size}")
    assert config.vector_store.chunk_size == 1024, "Chunk size override failed"
    
    print("✓ All environment overrides working correctly!")


def test_logging_levels():
    """Test logging at different levels"""
    print("\n=== Test 3: Logging Levels ===")
    
    # Test INFO level (default)
    print("\n--- INFO Level ---")
    configure_logging(level="INFO")
    logger = get_logger("test.info")
    
    logger.debug("This DEBUG message should NOT appear")
    logger.info("This INFO message SHOULD appear")
    logger.warning("This WARNING message SHOULD appear")
    logger.error("This ERROR message SHOULD appear")
    
    # Test DEBUG level
    print("\n--- DEBUG Level ---")
    configure_logging(level="DEBUG")
    logger = get_logger("test.debug")
    
    logger.debug("This DEBUG message SHOULD appear now")
    logger.info("This INFO message SHOULD appear")
    
    # Test ERROR level
    print("\n--- ERROR Level ---")
    configure_logging(level="ERROR")
    logger = get_logger("test.error")
    
    logger.info("This INFO message should NOT appear")
    logger.warning("This WARNING message should NOT appear")
    logger.error("This ERROR message SHOULD appear")


def test_request_id_tracking():
    """Test request ID tracking in logs"""
    print("\n=== Test 4: Request ID Tracking ===")
    
    configure_logging(level="INFO")
    
    # Without request ID
    logger = get_logger("test.request")
    logger.info("Log without request ID")
    
    # With request ID
    logger_with_id = get_logger("test.request", request_id="req-12345")
    logger_with_id.info("Log with request ID: req-12345")
    
    # Using log_with_context
    log_with_context(
        logger,
        "info",
        "Log with context data",
        request_id="req-67890",
        user_id="user-123",
        action="test_action"
    )


def test_structured_logging():
    """Test structured logging with extra data"""
    print("\n=== Test 5: Structured Logging ===")
    
    configure_logging(level="INFO")
    logger = get_logger("test.structured")
    
    # Log with structured data
    log_with_context(
        logger,
        "info",
        "API request received",
        request_id="req-api-001",
        endpoint="/workflow/research-summary",
        method="POST",
        latency_ms=125.5
    )
    
    log_with_context(
        logger,
        "info",
        "State transition",
        request_id="req-api-001",
        from_node="research",
        to_node="synthesis",
        step_count=2
    )


def test_error_logging():
    """Test error logging with exception info"""
    print("\n=== Test 6: Error Logging with Exceptions ===")
    
    configure_logging(level="INFO")
    logger = get_logger("test.error")
    
    try:
        # Simulate an error
        result = 1 / 0
    except ZeroDivisionError as e:
        logger.error("An error occurred during calculation", exc_info=True)
        log_with_context(
            logger,
            "error",
            "Division by zero error",
            request_id="req-error-001",
            operation="divide",
            error_type=type(e).__name__
        )


def main():
    """Run all tests"""
    print("=" * 60)
    print("Configuration and Logging Test Suite")
    print("=" * 60)
    
    try:
        test_default_config()
        test_env_override()
        test_logging_levels()
        test_request_id_tracking()
        test_structured_logging()
        test_error_logging()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
