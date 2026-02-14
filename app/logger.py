"""
Centralized Logging Module

Provides structured logging with rich console output and optional JSON formatting.
Supports configurable log levels and request ID tracking for observability.
"""

import logging
import sys
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console
import json
from datetime import datetime


# Global logger registry
_loggers: dict[str, logging.Logger] = {}
_log_level: str = "INFO"
_json_format: bool = False


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging in production.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add request_id if present
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "extra_data"):
            log_data["extra"] = record.extra_data
        
        return json.dumps(log_data)


def configure_logging(level: str = "INFO", json_format: bool = False) -> None:
    """
    Configure global logging settings.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        json_format: Use JSON format for logs (production mode)
    """
    global _log_level, _json_format
    
    _log_level = level.upper()
    _json_format = json_format
    
    # Reconfigure existing loggers
    for logger in _loggers.values():
        logger.setLevel(_log_level)
        
        # Update handlers
        for handler in logger.handlers:
            handler.setLevel(_log_level)


def get_logger(
    name: str,
    request_id: Optional[str] = None
) -> logging.Logger:
    """
    Get or create a logger instance with the specified name.
    
    Args:
        name: Logger name (typically __name__ of the module)
        request_id: Optional request ID for tracking
        
    Returns:
        Configured logger instance
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("System initialized")
        >>> 
        >>> # With request ID
        >>> logger = get_logger(__name__, request_id="req-123")
        >>> logger.info("Processing request")
    """
    # Return existing logger if already created
    if name in _loggers:
        logger = _loggers[name]
        
        # Update request_id if provided
        if request_id:
            logger = logging.LoggerAdapter(logger, {"request_id": request_id})
        
        return logger
    
    # Create new logger
    logger = logging.getLogger(name)
    logger.setLevel(_log_level)
    logger.propagate = False
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Configure handler based on format preference
    if _json_format:
        # JSON formatter for production
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
    else:
        # Rich handler for beautiful console output
        console = Console(stderr=False)
        handler = RichHandler(
            console=console,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            show_time=True,
            show_level=True,
            show_path=True,
            markup=True,
        )
        handler.setFormatter(
            logging.Formatter(
                "%(message)s",
                datefmt="[%X]"
            )
        )
    
    handler.setLevel(_log_level)
    logger.addHandler(handler)
    
    # Store in registry
    _loggers[name] = logger
    
    # Wrap with adapter if request_id provided
    if request_id:
        return logging.LoggerAdapter(logger, {"request_id": request_id})
    
    return logger


class LoggerContext:
    """
    Context manager for temporary logger configuration.
    
    Example:
        >>> with LoggerContext(request_id="req-456"):
        ...     logger = get_logger(__name__)
        ...     logger.info("Processing in context")
    """
    
    def __init__(self, request_id: Optional[str] = None):
        self.request_id = request_id
        self.original_adapters = {}
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def log_with_context(
    logger: logging.Logger,
    level: str,
    message: str,
    request_id: Optional[str] = None,
    **extra_data
) -> None:
    """
    Log a message with additional context data.
    
    Args:
        logger: Logger instance
        level: Log level (debug, info, warning, error)
        message: Log message
        request_id: Optional request ID
        **extra_data: Additional key-value pairs to include in log
        
    Example:
        >>> logger = get_logger(__name__)
        >>> log_with_context(
        ...     logger, "info", "User action",
        ...     request_id="req-789",
        ...     user_id="user-123",
        ...     action="login"
        ... )
    """
    log_func = getattr(logger, level.lower())
    
    # Create extra dict for structured data
    extra = {"extra_data": extra_data}
    if request_id:
        extra["request_id"] = request_id
    
    log_func(message, extra=extra)


# Initialize logging on module import
def _initialize_logging():
    """Initialize logging with default settings"""
    try:
        from app.config import get_config
        config = get_config()
        configure_logging(
            level=config.log.level,
            json_format=config.log.json_format
        )
    except Exception:
        # Fall back to defaults if config not available
        configure_logging(level="INFO", json_format=False)


# Auto-initialize when module is imported
_initialize_logging()
