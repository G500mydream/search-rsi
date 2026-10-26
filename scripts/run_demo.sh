#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"
PYTHONPATH="$project_root/src${PYTHONPATH:+:$PYTHONPATH}" python -m search_rsi.runner "$@"
