"""
Configuration Management Module

Loads system configuration from environment variables or YAML file.
Uses Pydantic BaseSettings for validation and type safety.
"""

import os
from typing import Literal, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


class LLMConfig(BaseSettings):
    """Configuration for Local LLM connection"""
    
    provider: Literal["ollama", "huggingface"] = Field(
        default="ollama",
        description="LLM provider to use"
    )
    model_name: str = Field(
        default="llama3",
        description="Name of the model to use for text generation"
    )
    embedding_model: str = Field(
        default="nomic-embed-text",
        description="Name of the model to use for embeddings"
    )
    base_url: str = Field(
        default="http://localhost:11434",
        description="Base URL for the LLM service"
    )
    timeout: int = Field(
        default=30,
        ge=1,
        description="Timeout in seconds for LLM requests"
    )
    
    model_config = SettingsConfigDict(
        env_prefix="LLM_",
        case_sensitive=False
    )


class VectorStoreConfig(BaseSettings):
    """Configuration for ChromaDB vector store"""
    
    persist_directory: str = Field(
        default="./chroma_db",
        description="Directory path for ChromaDB persistence"
    )
    collection_name: str = Field(
        default="documents",
        description="Name of the ChromaDB collection"
    )
    chunk_size: int = Field(
        default=512,
        ge=100,
        description="Size of document chunks in tokens"
    )
    chunk_overlap: int = Field(
        default=50,
        ge=0,
        description="Overlap between chunks in tokens"
    )
    
    model_config = SettingsConfigDict(
        env_prefix="VECTOR_",
        case_sensitive=False
    )


class RetryConfig(BaseSettings):
    """Configuration for retry logic and resiliency"""
    
    max_attempts: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum number of retry attempts"
    )
    min_wait: int = Field(
        default=2,
        ge=1,
        description="Minimum wait time in seconds for exponential backoff"
    )
    max_wait: int = Field(
        default=10,
        ge=1,
        description="Maximum wait time in seconds for exponential backoff"
    )
    
    model_config = SettingsConfigDict(
        env_prefix="RETRY_",
        case_sensitive=False
    )


class APIConfig(BaseSettings):
    """Configuration for FastAPI server"""
    
    host: str = Field(
        default="0.0.0.0",
        description="Host address to bind the API server"
    )
    port: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="Port number for the API server"
    )
    reload: bool = Field(
        default=False,
        description="Enable auto-reload for development"
    )
    
    model_config = SettingsConfigDict(
        env_prefix="API_",
        case_sensitive=False
    )


class LogConfig(BaseSettings):
    """Configuration for logging"""
    
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO",
        description="Logging level"
    )
    json_format: bool = Field(
        default=False,
        description="Use JSON format for logs (production)"
    )
    
    model_config = SettingsConfigDict(
        env_prefix="LOG_",
        case_sensitive=False
    )


class SystemConfig(BaseSettings):
    """Main system configuration aggregating all sub-configs"""
    
    llm: LLMConfig = Field(default_factory=LLMConfig)
    vector_store: VectorStoreConfig = Field(default_factory=VectorStoreConfig)
    retry: RetryConfig = Field(default_factory=RetryConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    log: LogConfig = Field(default_factory=LogConfig)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> "SystemConfig":
        """
        Load configuration from a YAML file.
        
        Args:
            yaml_path: Path to the YAML configuration file
            
        Returns:
            SystemConfig instance
            
        Raises:
            FileNotFoundError: If YAML file doesn't exist
            ValueError: If YAML is invalid or contains invalid config
        """
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"Configuration file not found: {yaml_path}")
        
        with open(yaml_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        
        if not config_dict:
            raise ValueError(f"Empty or invalid YAML file: {yaml_path}")
        
        return cls(**config_dict)
    
    @classmethod
    def load(cls, yaml_path: Optional[str] = None) -> "SystemConfig":
        """
        Load configuration with fallback logic:
        1. Try loading from YAML file if path provided
        2. Fall back to environment variables
        3. Use defaults if neither available
        
        Args:
            yaml_path: Optional path to YAML configuration file
            
        Returns:
            SystemConfig instance
        """
        if yaml_path and os.path.exists(yaml_path):
            try:
                return cls.from_yaml(yaml_path)
            except Exception as e:
                raise ValueError(f"Failed to load configuration from {yaml_path}: {e}")
        
        # Load from environment variables (with .env file support)
        return cls()


# Global configuration instance
_config: Optional[SystemConfig] = None


def get_config(yaml_path: Optional[str] = None, reload: bool = False) -> SystemConfig:
    """
    Get the global system configuration instance.
    
    Args:
        yaml_path: Optional path to YAML configuration file
        reload: Force reload of configuration
        
    Returns:
        SystemConfig instance
    """
    global _config
    
    if _config is None or reload:
        _config = SystemConfig.load(yaml_path)
    
    return _config
