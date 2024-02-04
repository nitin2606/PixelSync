import logging
from uvicorn import run
from app import app  

# Set the log level for uvicorn to WARNING
logging.getLogger("uvicorn").setLevel(logging.WARNING)

if __name__ == "__main__":
    # Run the FastAPI application
    run(app, host="0.0.0.0", port=8000, reload=True)


