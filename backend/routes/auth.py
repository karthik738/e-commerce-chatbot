from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from datetime import timedelta

# In-memory user store (use a proper database in production)
users_db = {}

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Router setup
router = APIRouter()

# Models
class User(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    message: str


class Settings(BaseModel):
    authjwt_secret_key: str = "18e6266a2deb655f11d4dcab386dfc95e77a360e262ba9f0c0635d0cbdc802b5"
    authjwt_access_token_expires: int = 60  # Token expiration time in minutes


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post("/register", response_model=UserOut)
async def register(user: User):
    """
    Register a new user.
    """
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered.")

    # Hash the password and store the user
    users_db[user.username] = pwd_context.hash(user.password)

    return {"username": user.username, "message": "User registered successfully."}


@router.post("/login")
async def login(user: User, Authorize: AuthJWT = Depends()):
    """
    Authenticate a user and return a JWT token.
    """
    # if user.username not in users_db:
        # raise HTTPException(status_code=401, detail="Invalid username or password.")

    # hashed_password = users_db[user.username]
    # if not pwd_context.verify(user.password, hashed_password):
        # raise HTTPException(status_code=401, detail="Invalid username or password.")

    hashed_password = users_db.get(user.username)
    if not hashed_password or not pwd_context.verify(user.password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")


    # Create the access token
    access_token = Authorize.create_access_token(
        subject=user.username, expires_time=timedelta(minutes=60)
    )

    return {"access_token": access_token, "token_type": "bearer"}
