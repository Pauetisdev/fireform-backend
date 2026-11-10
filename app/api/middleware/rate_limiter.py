from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Initialize the limiter using the client's IP address as the identifier
limiter = Limiter(key_func=get_remote_address)

def setup_rate_limiting(app: FastAPI) -> None:
    """Register rate limiting middleware and error handler on the FastAPI app."""
    
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    # Catch the specific SlowAPI exception to return a formatted JSON response
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
        return JSONResponse(
            status_code=429,
            content={
                "success": False,
                "error": "RATE_LIMIT_EXCEEDED",
                "message": f"Too many requests. Limit: {exc.detail}",
            },
        )