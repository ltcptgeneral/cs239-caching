import os
import uvicorn
from database import init_db  # Ensure database initializes before starting FastAPI
import logging

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

if __name__ == "__main__":
    # Initialize TinyDB (NoSQL) before FastAPI starts
    init_db()
    
    # Start the FastAPI server with custom options
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2, log_level=logging.WARNING)
