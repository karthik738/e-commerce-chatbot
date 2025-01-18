import logging
from fastapi import APIRouter, HTTPException,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from services.retrieval import retrieve_from_pinecone
from services.generation import generate_response_with_llm,summarize_with_openrouter
from services.embedding import init_vector_db

# Router setup
router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    history: list[dict] = []



def get_vector_db():
    """
    Dependency to initialize and return the Pinecone vector database connection.
    """
    return init_vector_db()

def preprocess_context(matches,limit=3):
    """
    Combine and preprocess retrieved chunks for the response generation.
    """
    combined_context = "\n".join(
        match["content"].strip() for match in matches[:limit] 
        # if match["content"]
    )
    return combined_context

def summarize_history(history):
    """
    Summarize the conversation history to retain key points.
    """
    if not history:
        return ""

    combined_history = " ".join(
        f"Q: {entry['query']} A: {entry['answer']}" for entry in history
    )

    # Here, we truncate the combined history for simplicity
    # Alternatively, call a summarization LLM API to condense the history
    summarized_history = combined_history[:500]  # Limit to 500 characters
    return summarized_history

# from transformers import GPT2Tokenizer
# # Load a tokenizer for token estimation (use GPT-2 tokenizer as it's compatible with most models)
# tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# def truncate_to_fit_model_limit(context, query, max_input_tokens=3000):
#     """
#     Ensure that the input tokens stay within the model's limit by truncating context.
#     Args:
#         context (str): The combined context for the model.
#         query (str): The user's query.
#         max_input_tokens (int): The maximum number of input tokens allowed.

#     Returns:
#         str: Truncated context if necessary.
#     """
#     # Tokenize context and query
#     context_tokens = tokenizer.encode(context, truncation=False)
#     query_tokens = tokenizer.encode(query, truncation=False)

#     # Calculate total tokens
#     total_tokens = len(context_tokens) + len(query_tokens)

#     # If tokens exceed the limit, truncate the context
#     if total_tokens > max_input_tokens:
#         excess_tokens = total_tokens - max_input_tokens
#         context_tokens = context_tokens[:-excess_tokens]  # Truncate excess tokens
#         logging.warning(f"Context truncated to fit within the model's token limit.")

#     # Decode tokens back to text
#     truncated_context = tokenizer.decode(context_tokens, skip_special_tokens=True)
#     return truncated_context


@router.post("/")
async def query_embeddings(request: QueryRequest, vector_db=Depends(get_vector_db)):
    """
    Endpoint for querying embeddings.
    """
    query = request.query.strip()
    history = request.history or [] # Include conversation history

    # logging.info(f"Query received: {query}")
    # logging.info(f"History: {history}")

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")



    try:
        

        # Retrieve matches from Pinecone
        matches = retrieve_from_pinecone(query,vector_db)
        # logging.info(f"Matches: {matches}")

        # Sort matches by relevance and preprocess context
        matches = sorted(matches, key=lambda x: x["score"], reverse=True)
        relevant_matches = [match for match in matches if match["score"] > 0.2]
        if not relevant_matches:
            return {
                "query": query,
                "answer": "No relevant information found in the knowledge base.",
                "history": history,
            }

        # Combine summarized history, recent conversation, and relevant context

        # Summarize older history if it exists
        summarized_history = ""
        if len(history) > 5:  # Only summarize if history is large
                summarized_history = summarize_with_openrouter(history[:-5])

        # summarized_history = ""
        # try:
            # if len(history) > 5:  # Only summarize if history is large
                # summarized_history = summarize_with_openrouter(history[:-5])
        # except Exception as e:
            # logging.warning(f"Summarization failed: {e}")
            # summarized_history = ""


        # summarized_history = summarize_history(history[:-5])  # Summarize older history
        # summarized_history = summarize_with_openrouter(history[:-5])  # Summarize older history
        # Alternative: Use local model or heuristic summarization
        # summarized_history = summarize_with_local_model(history[:-5])
        # summarized_history = summarize_with_heuristics(history[:-5])

        recent_history = history[-5:]  # Keep the last 5 exchanges intact
        recent_context = " ".join(
            f"Q: {entry['query']} A: {entry['answer']}" for entry in recent_history
        )

        combined_context = preprocess_context(relevant_matches)
        # logging.info(f"Combined context for query '{query}': {combined_context[:500]}")  # Log the first 500 characters

        # if not combined_context.strip():
        #     logging.warning("No context provided for generation. Returning default response.")
        #     return {"query": query, "answer": "No relevant information found in the knowledge base."}

        # Construct final context for the LLM
        context_for_llm = (
            f"Conversation Summary: {summarized_history}\n"
            f"Recent Conversation: {recent_context}\n"
            f"Relevant Context: {combined_context}"
        )

        # logging.info(f"Context for LLM: {context_for_llm[:500]}")

        # Ensure the context fits within token limits
        # truncated_context = truncate_to_fit_model_limit(context_for_llm, query)
        # answer = generate_response_with_llm(query, context=truncated_context)


        # Generate a response using the LLM
        answer = generate_response_with_llm(query, context=context_for_llm)
        
        # Append the new query and answer to the history
        history.append({"query": query, "answer": answer})

        return {"query": query, "answer": answer}

    except Exception as e:
        # logging.error(f"Error during query processing: {e}")
        return JSONResponse(
            content={"error": f"An internal error occurred: {str(e)}"},
            status_code=500,
        )

# @router.get("/")
# async def fun():
#     return {"message": "Welcome to the Query"} 