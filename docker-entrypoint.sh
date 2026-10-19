#!/bin/sh
set -e

echo "Starting Enterprise Knowledge Assistant..."

if [ ! -d "data/chroma" ] || [ -z "$(find data/chroma -mindepth 1 -print -quit 2>/dev/null)" ]; then
    echo "No Chroma index found."
    echo "Running document ingestion..."
    python -m src.ingest
else
    echo "Existing Chroma index found."
fi

exec streamlit run app.py \
    --server.address=0.0.0.0 \
    --server.port=8501 \
    --server.headless=true
