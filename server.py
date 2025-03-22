import uvicorn
from app.config import settings
from app.main import app

if __name__ == "__main__":
    # Run the server using Uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug
    )
