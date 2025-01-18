import os
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
import logging

MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_NAME = "ecommerce-chatbot"
DIMENSION = 384  # Dimension of embeddings generated by the model
METRIC = "cosine"  # Similarity metric

PINECONE_API_KEY="pcsk_5NqT9L_2TnqthjdeDQz38xJZJeZhwkzmGd68g6uGj1MsvtAi6LG532NqCRpXwojGWGeZb1"
# print(f"Pinecone api key: {PINECONE_API_KEY}")
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def init_vector_db():
    """Initialize Pinecone vector database."""
    try:
        # Fetch API key from environment variables
        # api_key = os.getenv("PINECONE_API_KEY")
        # if not api_key:
            # print("Pinecone API key not found. Please set 'PINECONE_API_KEY' as an environment variable.")

        # Create a Pinecone instance
        pc = Pinecone(api_key=PINECONE_API_KEY)

        # Check if the index exists, create it if it doesn't
        if INDEX_NAME not in pc.list_indexes().names():
            pc.create_index(
                name=INDEX_NAME,
                dimension=DIMENSION,
                metric=METRIC,
                spec=ServerlessSpec(
                    cloud="aws",  # Specify your cloud provider
                    region="us-east-1"  # Specify your desired region
                )
            )
            # logging.info(f"Index '{INDEX_NAME}' created.")
        # else:
            # logging.info(f"Index '{INDEX_NAME}' already exists.")

        return pc.Index(INDEX_NAME)

    except ValueError as ve:
        logging.error(ve)
        # raise
    except Exception as e:
        logging.error(f"Error initializing Pinecone: {e}")
        # raise

def generate_embeddings(chunks, vector_db, filename):
    """Generate embeddings for text chunks and store them in Pinecone with metadata."""
    try:
        # Check if chunks are empty
        if not chunks:
            logging.error(f"No chunks to process for file: {filename}")
            return

        # Log the first few chunks for debugging
        # logging.info(f"Chunks for {filename}: {chunks[:3]}")

        # Load the sentence transformer model
        model = SentenceTransformer(MODEL_NAME)

        # Generate embeddings for the chunks
        embeddings = model.encode(chunks)

        # Upsert embeddings with metadata (content included)
        vector_data = [
            (
                f"{filename}_{i}",  # Unique ID
                embedding.tolist(),  # Embedding vector
                {"filename": filename, "content": chunk}  # Metadata
            )
            for i, (embedding, chunk) in enumerate(zip(embeddings, chunks))
        ]
        vector_db.upsert(vectors=vector_data)
        logging.info(f"Embeddings generated and stored for {filename}")

    except Exception as e:
        logging.error(f"Failed to generate embeddings for {filename}: {e}")
        raise


def embeddings_exist(vector_db, filename):
    """Check if embeddings for a file already exist in Pinecone."""
    try:
        # Generate a unique ID for the first chunk
        test_id = f"{filename}_0"

        # Use `fetch` to check if the ID exists in Pinecone
        response = vector_db.fetch(ids=[test_id])

        # Log the fetch response for debugging
        # logging.info(f"Fetch response: {response}")

        # Check if the ID exists in the response
        return test_id in response.get("vectors", {})

    except Exception as e:
        logging.error(f"Error checking existence of embeddings for {filename}: {e}")
        raise
