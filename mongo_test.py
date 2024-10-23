from pymongo import MongoClient
import time

MONGODB_URL = "mongodb+srv://renex-client:anfas18@renex-dev.cpxve.mongodb.net/?retryWrites=true&w=majority&appName=renex-dev"

try:
    # Start the timer
    start_time = time.time()

    # Establish the connection
    client = MongoClient(MONGODB_URL)

    # Run the 'ping' command to check the connection
    client.admin.command('ping')

    # End the timer
    end_time = time.time()

    # Success message
    print(f"MongoDB connection successful! Connected in {end_time - start_time:.4f} seconds")

    db = client['my_database']
    collection = db['my_collection'] 

    # Update the document with name "Alice" to change its schema
    result = collection.update_one(
        {"name": "Alice"},  # Query to find the document
        {
            "$set": {          # Set new fields
                "regno": 1,    # Add regno field
                "name": "Alice",  # Update or retain name
                "email": "alice@example.com",  # Update or retain email
                "age": 50,     # Update age
                "location": "California"  # Update or retain location
            }
        }
    )

    if result.matched_count > 0:
        print("Document updated successfully.")
    else:
        print("No document matched the query.")

     # Check for existing entries with regno 2
    existing_dilna_list = list(collection.find({"regno": 2}))

    if len(existing_dilna_list) > 1:
        # Keep one and delete the others
        ids_to_delete = [doc["_id"] for doc in existing_dilna_list[1:]]  # Skip the first one

        delete_result = collection.delete_many({"_id": {"$in": ids_to_delete}})
        print(f"Deleted {delete_result.deleted_count} documents with regno 2, keeping one.")

    elif len(existing_dilna_list) == 1:
        print("Document with regno 2 already exists:", existing_dilna_list[0])
    else:
        # Insert a new document for Dilna if none exists
        dilna_entry = {
            "regno": 2, 
            "name": "Dilna",
            "email": "dilna@example.com",
            "age": 40,
            "location": "New York"
        }

        insert_result = collection.insert_one(dilna_entry)  # Insert the new entry

        if insert_result.inserted_id:
            print("Document for Dilna inserted successfully.")
        else:
            print("Failed to insert document for Dilna.")

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")


'''
-------------------------------------------------------------------
                WE DONT WANT THIS FUNCTION FOR NOW 
-------------------------------------------------------------------

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


'''