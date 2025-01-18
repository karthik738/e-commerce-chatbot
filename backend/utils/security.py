# import os
# from fastapi import HTTPException, Security
# from fastapi.security.api_key import APIKeyHeader
# from dotenv import load_dotenv

# # Load environment variables from a .env file
# load_dotenv()

# # Constants
# API_KEY_NAME = "X-API-KEY"
# EXPECTED_API_KEY = os.getenv("ADMIN_API_KEY")

# # API Key Header for authentication
# api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


# def validate_api_key(api_key: str = Security(api_key_header)):
#     """
#     Validate the provided API key for secure access.
#     """
#     if not api_key:
#         raise HTTPException(
#             status_code=401, detail="API key missing"
#         )

#     if api_key != EXPECTED_API_KEY:
#         raise HTTPException(
#             status_code=403, detail="Invalid API key"
#         )

#     return api_key
