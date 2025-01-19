import os
import logging
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
import aiofiles
from services.embedding import init_vector_db, embeddings_exist
from utils.file_utils import process_file

# Constants
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Router setup
router = APIRouter()

# Maximum file size (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Lazy initialization for vector database
_vector_db = None

def get_vector_db():
    """
    Initialize vector database lazily.
    """
    global _vector_db
    if _vector_db is None:
        # logging.info("Initializing vector database...")
        _vector_db = init_vector_db()
    return _vector_db


@router.post("/")
async def upload_files(
    files: list[UploadFile] = File(...), background_tasks: BackgroundTasks = None
):
    """
    Endpoint for uploading files.
    """
    vector_db = get_vector_db()  # Initialize vector_db lazily

    response_data = []
    for file in files:
        try:
            # Check file size manually
            file_size = 0
            async with aiofiles.open(os.path.join(UPLOAD_DIR, file.filename), "wb") as f:
                while content := await file.read(1024 * 1024):  # Read in 1MB chunks
                    file_size += len(content)
                    if file_size > MAX_FILE_SIZE:
                        raise HTTPException(
                            status_code=400,
                            detail=f"File {file.filename} exceeds size limit of 10 MB.",
                        )
                    await f.write(content)

            # Check if embeddings already exist
            if embeddings_exist(vector_db, file.filename):
                response_data.append(
                    {"filename": file.filename, "message": "Embeddings already exist, skipping processing."}
                )
                continue

            # Process the file in the background
            background_tasks.add_task(process_file, file.filename, os.path.join(UPLOAD_DIR, file.filename), vector_db)

            response_data.append({"filename": file.filename, "message": "File queued for processing"})
        except Exception as e:
            logging.error(f"Error processing file {file.filename}: {e}")
            response_data.append({"filename": file.filename, "error": str(e)})

    return {"files": response_data}
