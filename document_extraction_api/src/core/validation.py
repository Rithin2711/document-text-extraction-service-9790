from __future__ import annotations

from fastapi import HTTPException, UploadFile, status

# Maximum accepted upload size in bytes (10 MiB).
MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024

# Allowed file extensions (lowercase, without dot).
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}


def _get_extension(filename: str | None) -> str:
    """Return the lowercase extension for a filename, or empty string if none."""
    if not filename or "." not in filename:
        return ""
    return filename.rsplit(".", 1)[-1].lower()


def validate_upload_or_raise(file: UploadFile, file_size_bytes: int) -> str:
    """Validate upload properties and return the normalized extension.

    Raises:
        HTTPException: 400 for invalid/missing inputs, 415 for unsupported types.
    """
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file was provided. Upload a single file via multipart/form-data field 'file'.",
        )

    extension = _get_extension(file.filename)
    if not extension:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must have an extension (.pdf, .docx, .txt).",
        )

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{extension}'. Supported types: PDF, DOCX, TXT.",
        )

    if file_size_bytes <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    if file_size_bytes > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size is {MAX_UPLOAD_SIZE_BYTES} bytes.",
        )

    return extension
