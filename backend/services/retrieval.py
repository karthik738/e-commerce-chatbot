from sentence_transformers import SentenceTransformer
import pinecone
import logging

MODEL_NAME = "all-MiniLM-L6-v2"

# Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def retrieve_from_pinecone(query, vector_db, top_k=5):
    """Retrieve relevant chunks and their metadata from Pinecone."""
    try:
        model = SentenceTransformer(MODEL_NAME)
        query_embedding = model.encode(query)
        response = vector_db.query(
            vector=query_embedding.tolist(),
            top_k=top_k,
            include_metadata=True
        )

        # Log retrieved matches
        matches = []
        for match in response.get("matches", []):
            content = match.get("metadata", {}).get("content", "")
            # logging.info(f"Retrieved content: {content[:50]}")  # Log first 50 characters
            matches.append({"content": content, "score": match["score"],"metadata": match.get("metadata", {})})

        # logging.info(f"Total matches retrieved: {len(matches)}")


        return matches
    except Exception as e:
        logging.error(f"Error during retrieval from Pinecone: {e}")
        # raise


# def format_retrieved_chunks(matches):
#     """Format retrieved matches for readability."""
#     formatted_results = []
#     for match in matches:
#         try:
#             # Use 'id' if 'metadata' is not present
#             chunk_id = match.get("metadata", {}).get("chunk_id", "N/A")
#             content_snippet = match.get("content", "")[:50]  # First 50 characters
#             score = match.get("score", 0)
#             formatted_results.append({"chunk_id": chunk_id, "content_snippet": content_snippet,"score": score})
#         except KeyError as e:
#             # Log and skip malformed matches
#             print(f"Malformed match encountered: {match} (Error: {e})")
#     return formatted_results
