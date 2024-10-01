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
