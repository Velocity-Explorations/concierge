import os
from fastapi import Request, HTTPException, status

# For now the default behavior is to run unprotected if api_key is not defined
# If it is we authenticated against the X-API-Key header

async def api_key_middleware(request: Request, call_next):
    api_key = os.getenv("API_KEY")
    
    if api_key:
        request_api_key = request.headers.get("X-API-Key")
        
        if not request_api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key required"
            )
        
        if request_api_key != api_key:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid API key"
            )
    
    response = await call_next(request)
    return response