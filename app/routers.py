from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, PositiveFloat
from bson import ObjectId
from app.database import get_collection
from typing import List, Optional
from bson.errors import InvalidId 
import logging
from datetime import datetime

router = APIRouter()

# Models for the property structure
class Location(BaseModel):
    city: str
    address: str

class Image(BaseModel):
    url: str
    alt: str

# class Price(BaseModel):
#     amount: PositiveFloat  # Define the price amount

class Property(BaseModel):
    paid_ad: bool
    location: Location
    transactionType: str
    propertyType: str
    image: Image  # Assuming image is an object with url and alt attributes
    price: PositiveFloat 
    features: List[str]
    available: bool

class PropertyUpdate(BaseModel):
    paid_ad: Optional[bool] = None
    location: Optional[Location] = None
    transactionType: Optional[str] = None
    propertyType: Optional[str] = None
    image: Optional[Image] = None
    price: Optional[PositiveFloat] = None
    features: Optional[List[str]] = None
    available: Optional[bool] = None

# Helper function to convert MongoDB document to a JSON-friendly format
def convert_to_json(doc):
    doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    return doc

@router.post("/insert_property")
async def insert_property(property: Property):
    logging.info("Received property data: %s", property.dict())

    collection = get_collection("renex", "properties")  # Specify your database and collection names

    # Generate a unique property ID
    document_count = await collection.count_documents({})
    property_id = f"a{document_count + 1}"

    # Prepare the property entry with nested structure and default values where necessary
    property_entry = {
        "id": property_id,
        "paid_ad": property.paid_ad,  # Assuming 'paid_ad' is a field in your Property model
        "location": {
            "city": property.location.city if property.location else "Unknown City",
            "address": property.location.address if property.location else "No address provided"
        },
        "transactionType": property.transactionType,  # Ensure correct attribute name
        "propertyType": property.propertyType,  # Ensure correct attribute name
        "image": {
            "url": property.image.url if property.image else "default-image.png",
            "alt": f"Building in {property.location.city}" if property.location else "Default building image"
        },
        "price": float(property.price) if isinstance(property.price, (int, float, str)) else None,
        "features": property.features or [],  # Default to an empty list if 'features' is not provided
        "available": property.available if property.available is not None else True,  # Default availability
        "updatedAt": datetime.now() 
    }

    try:
        # Insert the property entry into the database
        result = await collection.insert_one(property_entry)
        return {
            "id": str(result.inserted_id),
            "location": property_entry["location"]["address"],
            "message": "Property added successfully!"
        }
    except Exception as e:
        logging.error("Error inserting property: %s", str(e))
        raise HTTPException(status_code=500, detail="Error inserting property into the database.")


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

    # Build update data
    update_data = {k: v for k, v in property.dict(exclude_unset=True).items()}
    
    try:
        result = await collection.update_one(
            {"id": property_id},  # Match by custom `id`
            {"$set": update_data}  # Set only fields that have been updated
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="No property matched the query.")
        
        # Optionally retrieve and return the updated document
        updated_property = await collection.find_one({"id": property_id})
        return {
            "message": "Property updated successfully.",
            "updated_property": convert_to_json(updated_property)
        }
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))