#!/bin/bash
set -e

echo "================================================"
echo " AGENCIA-V3 — Gates de Calidad"
echo "================================================"

echo ""
echo "=== Gate 1: Tests Unitarios ==="
pytest tests/unit/ -x -q --tb=short
echo "Gate 1: PASADO ✓"

echo ""
echo "=== Gate 2: Tests de Integración ==="
pytest tests/integration/ -x -q --tb=short
echo "Gate 2: PASADO ✓"

echo ""
echo "=== Gate 3: Cobertura ≥85% ==="
pytest tests/unit/ tests/integration/ \
  --cov=. --cov-fail-under=85 -q \
  --cov-omit="*/test_*,*/__pycache__/*,dashboard/*,export/*,agents/*,license-server/*,demos/*"
echo "Gate 3: PASADO ✓"

echo ""
echo "================================================"
echo " Todos los gates pasaron ✓"
echo "================================================"
