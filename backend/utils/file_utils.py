import os
import csv
from PyPDF2 import PdfReader
import logging
import unicodedata
from services.embedding import generate_embeddings

# Constants
EXTRACTED_DIR = "extracted_content"
os.makedirs(EXTRACTED_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def process_file(filename, file_path, vector_db, chunk_size=500):
    """
    Process a file: extract content, chunk it, and generate embeddings.
    """
    try:
        # Extract text based on file type
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif filename.endswith(".txt"):
            text = extract_text_from_txt(file_path)
        elif filename.endswith(".csv"):
            text = extract_text_from_csv(file_path)
        else:
            logging.warning(f"Unsupported file format: {filename}")
            return

        # Proceed if text is successfully extracted
        if text:
            text = normalize_text(text)
            save_extracted_content(filename, text)
            chunks = chunk_text(text, chunk_size)
            generate_embeddings(chunks, vector_db, filename)
        else:
            logging.warning(f"No text extracted from {filename}. File may be empty or unsupported.")

    except Exception as e:
        logging.error(f"Error processing file {filename}: {e}")


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.
    """
    try:
        reader = PdfReader(file_path)
        return "".join(page.extract_text() for page in reader.pages if page.extract_text())
    except Exception as e:
        logging.error(f"Failed to extract text from PDF: {e}")
        return None


def extract_text_from_txt(file_path):
    """
    Extract text from a plain text file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logging.error(f"Failed to extract text from TXT: {e}")
        return None


def extract_text_from_csv(file_path):
    """
    Extract text from a CSV file.
    """
    try:
        rows = []
        with open(file_path, "r", encoding="utf-8", errors="replace") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                rows.append(" ".join(row))
        return "\n".join(rows)
    except Exception as e:
        logging.error(f"Failed to extract text from CSV: {e}")
        return None


def normalize_text(text):
    """
    Normalize text for consistent processing.
    """
    return unicodedata.normalize("NFKC", text)


def chunk_text(text, chunk_size=500):
    """
    Split text into smaller chunks for embedding.
    """
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


def save_extracted_content(filename, content):
    """
    Save extracted content to a .txt file for verification.
    """
    try:
        output_filename = os.path.join(EXTRACTED_DIR, f"{os.path.splitext(filename)[0]}_extracted.txt")
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Extracted content saved: {output_filename}")
    except Exception as e:
        logging.error(f"Failed to save extracted content: {e}")
