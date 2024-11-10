#!/usr/bin/env bash
PYTHONPATH=. python scripts/create_doc.py > docs/openapi.json
git diff --exit-code docs/openapi.json
if [ $? -ne 0 ]
then
  echo "Api doc needs to be regenerated"
  exit 1
fi
