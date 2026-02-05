from pydantic import BaseModel, Field


class ExtractTextResponse(BaseModel):
    """Response payload for extracted document text."""

    text: str = Field(..., description="Extracted, readable text from the uploaded document.")
