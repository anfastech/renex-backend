from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_collection

router = APIRouter()

# Define a Pydantic model for the request body
class Name(BaseModel):
    name: str

class User(BaseModel):
    regno: int
    name: str
    email: str
    age: int
    location: str

# Helper function to convert MongoDB document to JSON-friendly format
def convert_to_json(doc):
    # Convert ObjectId and other non-serializable fields to strings or other serializable formats
    doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    if "age" in doc:
        doc["age"] = int(doc["age"])  # Convert any potential numeric fields properly
    if "regno" in doc:
        doc["regno"] = int(doc["regno"])  # Handle regno conversion if it's stored as a BSON type
    return doc

@router.post("/insert_alice")
async def insert_alice():
    collection = get_collection("my_database", "my_collection")  # Specify your database and collection names
    alice_entry = {
        "regno": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "age": 50,
        "location": "California",
    }
    try:
        result = await collection.insert_one(alice_entry)  # Insert Alice's entry
        return {"id": str(result.inserted_id), "name": alice_entry["name"]}
    except Exception as e:
        return {"error": str(e)}

@router.put("/update_alice/{regno}")
async def update_alice(regno: int):
    collection = get_collection("my_database", "my_collection")
    result = await collection.update_one(
        {"regno": regno},  # Find the document by regno
        {"$set": {"age": 50}}  # Update the age to 50
    )
    if result.matched_count > 0:
        return {"message": "Document updated successfully."}
    else:
        raise HTTPException(status_code=404, detail="No document matched the query.")

# @router.post("/dilna")
# async def create_dilna():
#     collection = get_collection("my_database", "my_collection")  # Specify your database and collection names
#     dilna_entry = {
#         "regno": 2,
#         "name": "Dilna",
#         "email": "dilna@example.com",
#         "age": 40,
#         "location": "New York",
#     }
    
#     # Check if Dilna already exists
#     existing_dilna = await collection.find_one({"regno": 2})
    
#     if existing_dilna:
#         # If Dilna exists, delete the existing entry
#         await collection.delete_one({"regno": 2})
    
#     # Insert the new entry for Dilna
#     try:
#         result = await collection.insert_one(dilna_entry)
#         return {"id": str(result.inserted_id), "name": dilna_entry["name"]}
#     except Exception as e:
#         return {"error": str(e)}

@router.get("/db-data")
async def get_names():
    collection = get_collection("my_database", "my_collection")  # Use your database and collection names
    cursor = collection.find()  # Fetch all documents
    names = await cursor.to_list(length=None)  # Convert cursor to a list
    
    # Apply the conversion function to all documents in the list
    converted_names = [convert_to_json(doc) for doc in names]

    return {"names": converted_names}  # Return all documents with BSON types converted to serializable types

# Helper function to extract the "name" field
def extract_name(doc):
    return doc.get("name", None)  # Safely get the 'name' field if it exists

@router.get("/names")
async def get_names():
    collection = get_collection("my_database", "my_collection")  # Use your database and collection names
    cursor = collection.find({}, {"name": 1, "regno": 1}).sort("regno", 1)  # Fetch only the "name" field from documents
    names = await cursor.to_list(length=None)  # Convert cursor to a list
    
    # Extract the "name" field from each document
    # name_list = [extract_name(doc) for doc in names]
    name_list = [{"name": doc["name"], "regno": doc["regno"]} for doc in names if "name" in doc and "regno" in doc]

    return {"names": name_list}  # Return only the names