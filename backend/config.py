# import os
# from dotenv import load_dotenv

# # Load environment variables from a .env file
# load_dotenv()

# # Pinecone Configuration
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1-gcp")  # Default environment

# # OpenRouter API Configuration
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# # Admin API Key for Security
# ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "default_admin_api_key")  # Replace the default value in production

# # Model Configuration
# EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")  # Default embedding model
# LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "meta-llama/llama-3.2-3b-instruct:free")  # Default LLM model

# # Other Constants
# UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_files")
# EXTRACTED_DIR = os.getenv("EXTRACTED_DIR", "extracted_content")
# MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 10))  # Default max file size: 10 MB
