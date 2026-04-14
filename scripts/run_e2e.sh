#!/bin/bash
echo "=== Gate 4: E2E con Ollama ==="
pytest tests/e2e/ -v --tb=short -s
echo "Gate 4 completado"
