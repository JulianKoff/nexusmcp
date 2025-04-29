from typing import Dict, Any, Optional
from pydantic import BaseSettings, Field
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings."""
    
    # Server settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Security settings
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Database settings
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    # Redis settings
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_PASSWORD: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    
    # Monitoring settings
    PROMETHEUS_METRICS_PORT: int = Field(default=9090, env="PROMETHEUS_METRICS_PORT")
    
    # Solana Configuration
    SOLANA_RPC_URL: str = Field(
        default=os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com"),
        env="SOLANA_RPC_URL"
    )
    SOLANA_WS_URL: str = Field(
        default=os.getenv("SOLANA_WS_URL", "wss://api.mainnet-beta.solana.com"),
        env="SOLANA_WS_URL"
    )
    SOLANA_DEVNET_RPC_URL: str = Field(
        default=os.getenv("SOLANA_DEVNET_RPC_URL", "https://api.devnet.solana.com"),
        env="SOLANA_DEVNET_RPC_URL"
    )
    SOLANA_DEVNET_WS_URL: str = Field(
        default=os.getenv("SOLANA_DEVNET_WS_URL", "wss://api.devnet.solana.com"),
        env="SOLANA_DEVNET_WS_URL"
    )
    
    # Program Addresses
    PROGRAM_ID_MAINNET: str = Field(
        default="7DVACb526KvzFkVffn4CURLpqgxQPcgbtiWUzSdAFPg8",
        env="PROGRAM_ID_MAINNET"
    )
    PROGRAM_ID_DEVNET: str = Field(
        default="HGXVvwP5F5LUCwwgnAaVLF4j8xionMgkxeZG5XNpfxe4",
        env="PROGRAM_ID_DEVNET"
    )
    
    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # Cache settings
    CACHE_TTL: int = Field(default=300, env="CACHE_TTL")  # 5 minutes
    
    # Rate limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=60, env="RATE_LIMIT_WINDOW")  # 1 minute
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Create necessary directories
def create_directories():
    """Create necessary directories for the application."""
    directories = [
        "logs",
        "data",
        "cache"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

# Initialize directories
create_directories() 