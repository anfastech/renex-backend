from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from bson import ObjectId
from app.database import get_collection
from typing import List, Optional

router = APIRouter()

# Define your PropertyUpdate model
class Location(BaseModel):
    city: str
    address: str

class Image(BaseModel):
    url: str
    alt: str

class PropertyUpdate(BaseModel):
    paid_ad: Optional[bool] = Field(default=None)
    location: Optional[Location] = Field(default=None)
    transactionType: Optional[str] = Field(default=None)
    propertyType: Optional[str] = Field(default=None)
    image: Optional[Image] = Field(default=None)
    price: Optional[int] = Field(default=None)
    features: Optional[List[str]] = Field(default=None)
    available: Optional[bool] = Field(default=None)

# Define a Pydantic model for Property
class Property(BaseModel):
    id: Optional[str] = None  # Make id optional
    paid_ad: bool
    location: dict
    transactionType: str
    propertyType: str
    image: dict
    price: float
    features: list
    available: bool

# Helper function to convert MongoDB document to JSON-friendly format
def convert_to_json(doc):
    doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    return doc

@router.post("/insert_property")
async def insert_property(property: Property):
    collection = get_collection("renex", "properties")  # Use your database and collection names
    
    # Calculate the document count to generate the ID
    document_count = await collection.count_documents({})
    property_id = f"a{document_count + 1}"  # Incrementing by 1 to make the ID unique

    # Add the new ID to the property dictionary
    property_entry = property.dict()
    property_entry['id'] = property_id  # Set the new ID

    try:
        result = await collection.insert_one(property_entry)  # Insert the property entry
        return {"id": str(result.inserted_id), "location": property_entry["location"]["address"]}
    except Exception as e:
        return {"error": str(e)}

@router.get("/properties")
async def get_properties():
    collection = get_collection("renex", "properties")
    cursor = collection.find()
    properties = await cursor.to_list(length=None)  # Convert cursor to a list

    # Apply the conversion function to all documents in the list
    converted_properties = [convert_to_json(doc) for doc in properties]

    return {"properties": converted_properties}

# Route to update the property by its 'id' field
@router.put("/update_property_by_id/{property_id}")
async def update_property_by_id(property_id: str, property: PropertyUpdate):
    collection = get_collection("renex", "properties")
    try:
        object_id = ObjectId(property_id)  # Convert string to ObjectId
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    
    update_data = property.dict(exclude_unset=True)  # Only include fields that are set
    result = await collection.update_one(
        {"_id": object_id},  # Query by ObjectId
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="No property matched the query.")
    
    # Optionally retrieve the updated document and return it
    updated_property = await collection.find_one({"_id": object_id})
    
    return {
        "message": "Property updated successfully.",
        "updated_property": convert_to_json(updated_property)
    }
