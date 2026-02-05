from __future__ import annotations

import io
from typing import Final

from fastapi import HTTPException, status
from pypdf import PdfReader
from docx import Document


class TextExtractionError(RuntimeError):
    """Raised when text extraction fails for a supported document type."""


_WHITESPACE_NORMALIZATION_MAX_NEWLINES: Final[int] = 2


def _normalize_text(text: str) -> str:
    """Normalize output to be more readable while preserving structure."""
    # Collapse Windows newlines and strip trailing whitespace lines.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Avoid huge runs of blank lines.
    lines = text.split("\n")
    normalized_lines: list[str] = []
    blank_run = 0
    for line in lines:
        if line.strip() == "":
            blank_run += 1
            if blank_run <= _WHITESPACE_NORMALIZATION_MAX_NEWLINES:
                normalized_lines.append("")
        else:
            blank_run = 0
            normalized_lines.append(line.rstrip())

    return "\n".join(normalized_lines).strip()


def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(io.BytesIO(content))
        parts: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                parts.append(page_text)
        return _normalize_text("\n\n".join(parts))
    except Exception as exc:  # noqa: BLE001
        raise TextExtractionError(f"Failed to extract text from PDF: {exc}") from exc


def extract_text_from_docx(content: bytes) -> str:
    """Extract text from a DOCX file."""
    try:
        doc = Document(io.BytesIO(content))
        parts = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
        return _normalize_text("\n".join(parts))
    except Exception as exc:  # noqa: BLE001
        raise TextExtractionError(f"Failed to extract text from DOCX: {exc}") from exc


def extract_text_from_txt(content: bytes) -> str:
    """Extract text from a TXT file, attempting UTF-8 with fallback."""
    # Try utf-8 first (common case). If that fails, replace invalid bytes.
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = content.decode("utf-8", errors="replace")
    return _normalize_text(text)


# PUBLIC_INTERFACE
def extract_text_or_http_500(extension: str, content: bytes) -> str:
    """Extract text from supported content, raising HTTP 500 on extraction errors.

    Args:
        extension: One of 'pdf', 'docx', 'txt'.
        content: Raw file bytes.

    Returns:
        Extracted text.

    Raises:
        HTTPException: 500 if extraction fails unexpectedly.
    """
    try:
        if extension == "pdf":
            return extract_text_from_pdf(content)
        if extension == "docx":
            return extract_text_from_docx(content)
        if extension == "txt":
            return extract_text_from_txt(content)

        # Should not happen if validation is done earlier.
        raise TextExtractionError(f"Unsupported extension '{extension}'")
    except TextExtractionError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
