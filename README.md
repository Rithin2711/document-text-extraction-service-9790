# Document Text Extraction Service

FastAPI backend service that accepts a **single uploaded document** (PDF, DOCX, or TXT) and returns extracted readable text as JSON.

## API

### `POST /extract-text`

- **Content-Type:** `multipart/form-data`
- **Field name:** `file`
- **Supported file types:** `.pdf`, `.docx`, `.txt`
- **Response:** `{"text": "..."}`

#### Error codes

- **400**: Validation errors (missing file, missing extension, empty file, file too large)
- **415**: Unsupported file type
- **500**: Extraction errors

## Usage examples (curl)

### Extract from PDF

```bash
curl -s -X POST "http://localhost:3001/extract-text" \
  -F "file=@./example.pdf" | jq
```

### Extract from DOCX

```bash
curl -s -X POST "http://localhost:3001/extract-text" \
  -F "file=@./example.docx" | jq
```

### Extract from TXT

```bash
curl -s -X POST "http://localhost:3001/extract-text" \
  -F "file=@./example.txt" | jq
```

## Local development

The service is configured to run on **port 3001** in this workspace environment. Use the interactive docs at:

- Swagger UI: `http://localhost:3001/docs`
- OpenAPI JSON: `http://localhost:3001/openapi.json`
"""
