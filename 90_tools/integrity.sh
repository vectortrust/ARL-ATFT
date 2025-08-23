#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT="${1:-}"; CMD="${2:-update}" # update|verify
[[ -z "$PROJECT" ]] && { echo "usage: $0 <project> [update|verify]"; exit 1; }
P_DIR="$ROOT/10_projects/$PROJECT"; [[ -d "$P_DIR" ]] || { echo "no such project: $PROJECT"; exit 2; }
shopt -s nullglob
files=("$P_DIR"/*.yaml "$P_DIR"/*.yml "$P_DIR"/*.md)
manifest="$P_DIR/manifest.yaml"
update_hashes(){ : > "$manifest.tmp"
  echo "project: $PROJECT" >> "$manifest.tmp"
  echo "last_updated: $(date -u +%FT%TZ)" >> "$manifest.tmp"
  echo "files:" >> "$manifest.tmp"
  for f in "${files[@]}"; do
    [[ "$(basename "$f")" == "manifest.yaml" ]] && continue
    sum=$(sha256sum "$f" | awk '{print $1}')
    echo "  - name: $(basename "$f")" >> "$manifest.tmp"
    echo "    sha256: $sum" >> "$manifest.tmp"
    echo "$sum  $f" > "$f.sha256"
  done
  mv "$manifest.tmp" "$manifest"
  echo "SHA256 ($manifest) = $(sha256sum "$manifest" | awk '{print $1}')" > "$manifest.sha256"
  if gpg --list-secret-keys >/dev/null 2>&1; then gpg --armor --detach-sign --output "$manifest.asc" "$manifest" || true; fi
  echo "Updated manifest + checksums for $PROJECT"
}
verify_hashes(){ ok=0
  for f in "${files[@]}"; do
    [[ -f "$f.sha256" ]] || { echo "MISSING: $f.sha256"; ok=1; continue; }
    sha256sum --check --status "$f.sha256" || { echo "FAIL: $f"; ok=1; }
  done
  [[ -f "$manifest.sha256" ]] && sha256sum --check --status "$manifest.sha256" || { echo "FAIL: manifest"; ok=1; }
  if [[ -f "$manifest.asc" ]]; then gpg --verify "$manifest.asc" "$manifest" && echo "GPG OK: manifest" || { echo "GPG FAIL"; ok=1; }; fi
  exit $ok
}
case "$CMD" in update) update_hashes ;; verify) verify_hashes ;; *) echo "unknown cmd: $CMD"; exit 3 ;; esac
