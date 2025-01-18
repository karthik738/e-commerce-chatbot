import logging
from fastapi import FastAPI
from routes.upload import router as upload_router
from routes.query import router as query_router
from routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# List of allowed origins
origins = [
    "http://localhost:3000",  # Frontend development server
    "http://localhost:8501"  # Add your production domain here
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
# Include the auth router
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])


# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to the RAG Chatbot Backend"}
