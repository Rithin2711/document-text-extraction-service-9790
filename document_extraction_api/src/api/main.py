from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import extraction_router

openapi_tags = [
    {
        "name": "System",
        "description": "Health checks and service metadata.",
    },
    {
        "name": "Extraction",
        "description": "Upload documents and extract readable text.",
    },
]

app = FastAPI(
    title="Document Text Extraction API",
    description=(
        "A FastAPI service that accepts PDF/DOCX/TXT uploads and returns extracted readable text as JSON.\n\n"
        "Use `POST /extract-text` with multipart/form-data field name `file`."
    ),
    version="1.0.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    tags=["System"],
    summary="Health Check",
    description="Simple health check endpoint to verify the service is running.",
    operation_id="health_check__get",
)
def health_check():
    """Health check endpoint.

    Returns:
        A small JSON payload indicating the service is healthy.
    """
    return {"message": "Healthy"}


app.include_router(extraction_router)
