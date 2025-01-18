import logging
from fastapi import FastAPI
from routes.upload import router as upload_router
from routes.query import router as query_router
from routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
import os

# Logging configuration
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout  # Ensure logs are sent to stdout
)


logging.info("before FastAPI application")

# Initialize FastAPI app
app = FastAPI(debug=True)

logging.info("afterr the FastAPI application")

# List of allowed origins
origins = [
    "http://localhost:3000",  # Frontend development server
    "http://localhost:8501",  # Streamlit development server
    "https://e-commerce-chatbot-black.vercel.app/",
    "https://e-commerce-chatbot.streamlit.app/",
    "https://e-commerce-chatbot-production.up.railway.app/",
]

logging.info("after origins")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origins that are allowed
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
logging.info("Starting after middleware")


# Include routers
app.include_router(upload_router, prefix="/upload", tags=["File Upload"])
logging.info("after uplaod")

app.include_router(query_router, prefix="/query", tags=["Query"])
logging.info("after query")

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
logging.info("after auth")


# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to the RAG Chatbot Backend"}


logging.info("after root")

# Lazy-loading of resources to optimize memory
vector_db = None

def get_vector_db():
    global vector_db
    if vector_db is None:
        from services.embedding import init_vector_db
        vector_db = init_vector_db()
    return vector_db

logging.info("after vector db function")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Fallback to 8000 if PORT is not set
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="debug")



