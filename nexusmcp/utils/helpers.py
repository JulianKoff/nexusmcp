from typing import Any, Dict, List, Optional
import json
import hashlib
import time
from datetime import datetime
import logging
from pathlib import Path
import asyncio
from functools import wraps
import random
import string

logger = logging.getLogger(__name__)

def generate_id(length: int = 16) -> str:
    """Generate a random ID."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def hash_data(data: Any) -> str:
    """Generate a hash for the given data."""
    if isinstance(data, (dict, list)):
        data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(str(data).encode()).hexdigest()

def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp to ISO format."""
    return timestamp.isoformat()

def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse ISO format timestamp."""
    return datetime.fromisoformat(timestamp_str)

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator for retrying functions."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay * (2 ** attempt))  # Exponential backoff
                        logger.warning(f"Retrying {func.__name__} (attempt {attempt + 1}/{max_attempts})")
            raise last_exception
        return wrapper
    return decorator

def cache_result(ttl: int = 300):
    """Decorator for caching function results."""
    def decorator(func):
        cache = {}
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = hash_data((args, kwargs))
            current_time = time.time()
            
            if key in cache:
                result, timestamp = cache[key]
                if current_time - timestamp < ttl:
                    return result
            
            result = await func(*args, **kwargs)
            cache[key] = (result, current_time)
            return result
        
        return wrapper
    return decorator

def validate_json(data: str) -> bool:
    """Validate if a string is valid JSON."""
    try:
        json.loads(data)
        return True
    except json.JSONDecodeError:
        return False

def format_error(error: Exception) -> Dict[str, Any]:
    """Format error for API response."""
    return {
        "error": str(error),
        "type": error.__class__.__name__,
        "timestamp": format_timestamp(datetime.utcnow())
    }

def calculate_percentage(value: float, total: float) -> float:
    """Calculate percentage."""
    if total == 0:
        return 0.0
    return (value / total) * 100

def format_bytes(size: int) -> str:
    """Format bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def ensure_directory(path: str) -> None:
    """Ensure directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)

def get_file_extension(filename: str) -> str:
    """Get file extension."""
    return Path(filename).suffix.lower()

def is_valid_address(address: str) -> bool:
    """Validate Ethereum address."""
    if not address.startswith("0x"):
        return False
    if len(address) != 42:
        return False
    try:
        int(address, 16)
        return True
    except ValueError:
        return False

def format_wei_to_eth(wei: int) -> float:
    """Convert Wei to ETH."""
    return wei / 10**18

def format_eth_to_wei(eth: float) -> int:
    """Convert ETH to Wei."""
    return int(eth * 10**18)

def calculate_gas_cost(gas_used: int, gas_price: int) -> float:
    """Calculate gas cost in ETH."""
    return format_wei_to_eth(gas_used * gas_price)

def generate_nonce() -> str:
    """Generate a random nonce."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def validate_signature(message: str, signature: str, address: str) -> bool:
    """Validate Ethereum signature."""
    # Implementation for signature validation
    # This is a placeholder - implement actual signature validation
    return True

def format_chain_id(chain_id: int) -> str:
    """Format chain ID to human-readable format."""
    chain_names = {
        1: "Ethereum Mainnet",
        137: "Polygon",
        42161: "Arbitrum",
        10: "Optimism",
        56: "BSC"
    }
    return chain_names.get(chain_id, f"Chain {chain_id}")

def calculate_risk_score(factors: Dict[str, float]) -> float:
    """Calculate risk score based on various factors."""
    weights = {
        "liquidity": 0.3,
        "volume": 0.2,
        "age": 0.1,
        "audit": 0.2,
        "community": 0.2
    }
    
    score = 0.0
    for factor, weight in weights.items():
        if factor in factors:
            score += factors[factor] * weight
            
    return min(max(score, 0.0), 1.0)  # Ensure score is between 0 and 1 