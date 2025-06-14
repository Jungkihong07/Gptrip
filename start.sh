#!/bin/bash
poetry install --no-root
export PYTHONPATH=app
poetry run uvicorn app.main:app --host=0.0.0.0 --port=8000
