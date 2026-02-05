#!/bin/bash
cd /home/kavia/workspace/code-generation/document-text-extraction-service-9790/document_extraction_api
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

