from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.users_routers import router as users_router  # Import the users router
from app.routers.property_routers import router as property_router  # Import the properties router
from app.routers.presigned_url_router import router as generate_presigned_url
from app.database import get_collection, get_mongo_client  # Import MongoDB client
from app.routers import upload

app = FastAPI()

# Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://renex-backend.onrender.com",  # Replace with your actual Render domain
        "https://renexapp.vercel.app",         # Vercel domain for your frontend
        "http://localhost:3000"                # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router, prefix="/users", tags=["users"])  # Users router
app.include_router(property_router, prefix="/properties", tags=["properties"])  # Properties router
# Register routers
app.include_router(generate_presigned_url, prefix="/api/s3", tags=["S3"])
# app.include_router(user_router.router, prefix="/api/users", tags=["Users"])
# app.include_router(upload.router)

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

