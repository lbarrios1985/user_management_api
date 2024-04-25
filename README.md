# User Management API

A RESTful API for user management built with FastAPI. Provides CRUD operations, proper validation, error handling, and is ready for deployment on Google Cloud Run.

## Features
- Full CRUD for users
- SQL database integration (default: SQLite)
- Input validation and error handling
- OpenAPI/Swagger docs with examples
- Logging
- Pytest-based tests
- Cloud Build config for GCP

## Quickstart
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run locally:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Run tests:
   ```bash
   pytest
   ```

## Deployment
See `cloudbuild.yaml` for GCP deployment steps.
