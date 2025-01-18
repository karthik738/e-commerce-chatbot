import logging
from openai import OpenAI

# Constants
API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "meta-llama/llama-3.2-3b-instruct:free"

# Initialize OpenRouter client
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def summarize_with_openrouter(history):
    """
    Summarize the history using OpenRouter API.
    """
    try:
        # Combine the conversation history into a single text
        combined_history = " ".join(
            f"Q: {entry['query']} A: {entry['answer']}" for entry in history
        )

        # Construct the prompt for summarization
        prompt = (
            f"Summarize the following chat history, retaining the most relevant information:\n\n"
            f"{combined_history}"
        )

        # Call the OpenRouter API
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",
                "X-Title": "<YOUR_SITE_NAME>",
            },
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant trained to summarize chat histories.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        # Extract and return the response content
        response = completion.choices[0].message.content.strip()
        logging.info(f"Summarized history: {response}")
        return response

    except Exception as e:
        logging.error(f"Error during summarization: {e}")
        return "Summary unavailable due to an error."

from transformers import pipeline

# Load the summarization model
summarizer = pipeline("summarization", model="google/flan-t5-base")

def summarize_with_local_model(history):
    """
    Summarize the history using a locally hosted model.
    """
    try:
        combined_history = " ".join(
            f"Q: {entry['query']} A: {entry['answer']}" for entry in history
        )

        # Use the model to summarize
        summary = summarizer(combined_history, max_length=100, min_length=30, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        logging.error(f"Error during local summarization: {e}")
        return "Summary unavailable due to an error."


def summarize_with_heuristics(history):
    """
    Summarize the history using basic heuristics (extractive summarization).
    """
    try:
        # Select only the most recent N exchanges
        recent_history = history[-5:]

        # Extract keywords from older history
        older_history = history[:-5]
        keywords = " ".join(
            f"Q: {entry['query']} A: {entry['answer']}" for entry in older_history
        )[:500]  # Limit to 500 characters

        # Combine recent and keyword-based history
        summary = f"Recent: {recent_history} Keywords: {keywords}"
        return summary
    except Exception as e:
        logging.error(f"Error during heuristic summarization: {e}")
        return "Summary unavailable due to an error."


def generate_response_with_llm(query, context):
    """
    Generate a response using the OpenRouter API based on the query and retrieved matches.
    """
    try:
        # Prepare context from relevant matches
        # context = "\n".join(
        #     f"{match['content']}" for match in relevant_matches[:3]  # Top 3 matches
        # )
        # if not context:
            # logging.warning("No context provided for generation. Returning default response.")
            # return "No relevant information found to generate a response."

        # Construct the prompt
        prompt = (
            f"Context:\n{context}\n\n"
            f"User Query: {query}\n\n"
            f"Provide a helpful, concise response based on the context."
        )
        logging.info(f"Prompt constructed for LLM: {prompt[:500]}")  # Log the first 500 characters


        # Call the OpenRouter API
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional: For rankings on openrouter.ai
                "X-Title": "<YOUR_SITE_NAME>",  # Optional: For rankings on openrouter.ai
            },
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant trained to answer questions based on provided context.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        # Extract and return the response content
        response = completion.choices[0].message.content.strip()
        logging.info(f"Generated response: {response}")
        return response

    except Exception as e:
        logging.error(f"Error during response generation: {e}")
        return "An error occurred while generating the response. Please try again later."
