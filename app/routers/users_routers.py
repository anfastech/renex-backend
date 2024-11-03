from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Any
import logging
from app.database import get_collection  # Ensure this is correctly imported

router = APIRouter()

# Define the User model with required fields
class User(BaseModel):
    email: EmailStr
    name: str
    phone: str
    country: str
    state: str
    district: str
    mainTown: str

# Function to insert a user into the database
async def insert_user_to_db(user: User) -> Any:
    try:
        collection = get_collection("renex", "users") # This should connect to the MongoDB collection
        result = await collection.insert_one(user.dict())
        return result.inserted_id
    except Exception as e:
        logging.error(f"Failed to insert user: {e}")
        raise HTTPException(status_code=500, detail="Database insertion failed")

@router.post("/insert_user", response_model=str)
async def insert_user(user: User):
    try:
        # Insert user into the database
        user_id = await insert_user_to_db(user)
        return str(user_id)  # Return just the ID as a string
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
