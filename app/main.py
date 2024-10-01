from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router
from app.database import get_collection, get_mongo_client  # Import Mongo client

app = FastAPI()

# Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(router)

# Global variable to store MongoDB connection status
mongo_status = "Unknown"

# Check MongoDB connection at startup
@app.on_event("startup")
async def check_mongo_connection():
    global mongo_status
    try:
        # Get MongoDB client
        client = get_mongo_client()

        # Use the 'admin' database to run the 'ping' command
        await client.admin.command("ping")
        mongo_status = "MongoDB is connected."
    except Exception as e:
        mongo_status = f"Failed to connect to MongoDB: {e}"

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI backend!", "mongo_status": mongo_status}
