from __future__ import annotations

from fastapi import APIRouter, File, UploadFile
from starlette import status

from src.core.validation import validate_upload_or_raise
from src.schemas.extraction import ExtractTextResponse
from src.services.text_extraction import extract_text_or_http_500

router = APIRouter(tags=["Extraction"])


@router.post(
    "/extract-text",
    response_model=ExtractTextResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract readable text from an uploaded document",
    description=(
        "Upload a single document file (PDF, DOCX, or TXT) using multipart/form-data field `file`. "
        "Returns extracted readable text as JSON."
    ),
    operation_id="extract_text__post",
)
async def extract_text(file: UploadFile = File(...)) -> ExtractTextResponse:
    """Extract readable text from a single uploaded file.

    Accepts:
        - multipart/form-data with a single file field named `file`
        - supported types: PDF (.pdf), DOCX (.docx), TXT (.txt)

    Returns:
        JSON object: {"text": "<extracted text>"}.

    Error handling:
        - 400: validation errors (missing file, empty file, file too large, missing extension)
        - 415: unsupported file types
        - 500: extraction errors
    """
    # Read the file once; also gives us the actual size regardless of client headers.
    content = await file.read()
    extension = validate_upload_or_raise(file=file, file_size_bytes=len(content))

    text = extract_text_or_http_500(extension=extension, content=content)
    return ExtractTextResponse(text=text)
