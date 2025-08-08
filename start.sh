#!/usr/bin/env bash
set -e

PORT=${PORT:-8501}

streamlit run main.py --server.port "$PORT" --server.address 0.0.0.0
