import logging
from fastapi import FastAPI
from routes.upload import router as upload_router
from routes.query import router as query_router
from routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
import os

# Initialize FastAPI app
app = FastAPI()

# List of allowed origins
origins = [
    "http://localhost:3000",  # Frontend development server
    "http://localhost:8501",  # Streamlit development server
    "https://e-commerce-chatbot-black.vercel.app/",
    "https://e-commerce-chatbot.streamlit.app/"
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origins that are allowed
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(upload_router, prefix="/upload", tags=["File Upload"])
app.include_router(query_router, prefix="/query", tags=["Query"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to the RAG Chatbot Backend"}

# Lazy-loading of resources to optimize memory
vector_db = None

def get_vector_db():
    global vector_db
    if vector_db is None:
        from services.embedding import init_vector_db
        vector_db = init_vector_db()
    return vector_db

# Main block for running the app
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Fallback to 8000 if PORT is not set
    logging.info(f"Starting server on port {port}...")
    uvicorn.run("main:app", host="0.0.0.0", port=port)
