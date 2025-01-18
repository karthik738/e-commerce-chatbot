from transformers import pipeline

# Load the conversational model
def load_llm_model():
    """
    Load a conversational model using Hugging Face's transformers library.
    This can be switched to any suitable model available on Hugging Face.
    """
    return pipeline("text2text-generation", model="google/flan-t5-small")

# Initialize the model
llm_model = load_llm_model()

def generate_response_with_llm(question, retrieved_chunks):
    """
    Use a local LLM to generate a response based on retrieved chunks.
    :param question: User's query.
    :param retrieved_chunks: Relevant chunks retrieved from the vector database.
    :return: Generated response.
    """
    try:
        # Prepare the prompt with the retrieved context
        context = "\n".join(retrieved_chunks)
        prompt = (
            f"The following information is retrieved from the knowledge base:\n\n"
            f"{context}\n\n"
            f"Question: {question}\n"
            f"Answer the question based on the above information."
        )
        
        # Generate a response
        result = llm_model(prompt, max_length=200, num_return_sequences=1)
        return result[0]["generated_text"].strip()
    except Exception as e:
        return f"Error generating response: {e}"
