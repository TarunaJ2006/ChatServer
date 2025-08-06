import uvicorn
from app import app

if __name__ == "__main__":
    # Run the server on all network interfaces
    uvicorn.run(
        "app:app",
        host="0.0.0.0",  # Listen on all available network interfaces
        port=8000,
        reload=True,     # Auto-reload on code changes
        log_level="info"
    )
