# Backend Application ( FaskAPI API, pydantic, boto3 , motor )

### Getting Started

These instructions will help you set up and run the backend locally on your machine.

### Prerequisites
- **Python** (version 3.7 or higher)
- **.env** (create a `.env` file in the project root and add your environment variables `credentials`)

To install the dependencies

```bash
pip install -r requirements.txt
```

### unning the Backend ( In root folder `backend`)

```bash
uvicorn app.main:app --reload
```

This command will:
- Launch the API in development mode (auto-reload on changes)
- Run the API on http://127.0.0.1:8000

### Project Structure
- app/
 - main.py: The main entry point for the FastAPI application.
 - routers/: Directory containing route files for different API endpoints.
 - database.py: Contains database connection setup.
 - __init__.py: Initializes the app package.

### API Documentation
FastAPI automatically generates documentation for your API. Once the server is running, you can access it at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## License
This project is licensed under the MIT License - see the LICENSE file for details.