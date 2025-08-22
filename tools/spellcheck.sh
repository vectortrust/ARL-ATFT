#!/usr/bin/env bash
set -euo pipefail
if ! command -v codespell >/dev/null 2>&1; then python3 -m pip install --user --upgrade codespell >/dev/null; fi
codespell "${@:-.}"
