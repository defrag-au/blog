#!/usr/bin/env bash
# Full site build: OG share cards → zola → public/
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 scripts/generate-og-cards.py
exec zola build "$@"
