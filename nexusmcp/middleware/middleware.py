from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
import time
import logging
from typing import Callable, Awaitable
import json
from ..config.settings import settings

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url}")
        if request.headers.get("content-type") == "application/json":
            try:
                body = await request.body()
                logger.debug(f"Request body: {body.decode()}")
            except Exception as e:
                logger.error(f"Error logging request body: {e}")
                
        # Process request
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} - "
            f"Processed in {process_time:.2f}s"
        )
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting."""
    
    def __init__(self, app, redis_client):
        super().__init__(app)
        self.redis = redis_client
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host
        
        # Check rate limit
        key = f"rate_limit:{client_ip}"
        current = await self.redis.get(key)
        
        if current is None:
            await self.redis.setex(
                key,
                settings.RATE_LIMIT_WINDOW,
                1
            )
        else:
            current = int(current)
            if current >= settings.RATE_LIMIT_REQUESTS:
                return Response(
                    content=json.dumps({"error": "Rate limit exceeded"}),
                    status_code=429,
                    media_type="application/json"
                )
            await self.redis.incr(key)
            
        return await call_next(request)

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for handling errors."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            return Response(
                content=json.dumps({
                    "error": "Internal server error",
                    "detail": str(e)
                }),
                status_code=500,
                media_type="application/json"
            )

class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware for security headers."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response

def setup_middleware(app):
    """Setup all middleware components."""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure appropriately for production
    )
    
    # Session middleware
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.JWT_SECRET,
        session_cookie="nexusforge_session",
        max_age=1800  # 30 minutes
    )
    
    # Custom middleware
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(SecurityMiddleware)
    
    # Rate limit middleware (requires Redis)
    if hasattr(app.state, "redis"):
        app.add_middleware(RateLimitMiddleware, redis_client=app.state.redis) 