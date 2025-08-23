#!/usr/bin/env bash
# bootstrap_repo.sh — create & populate a VectorTrust repo in one go
# Usage:
#   ./bootstrap_repo.sh <repo-name> [--public|--private] [--slug <project_slug>]
# Defaults: --private, slug=seed_<yyyymmdd>
set -euo pipefail

GH_USER="vectortrust"
BASE="/home/nfs/vtrust"
TEMPLATE="$BASE/atlas-memory-trust"

need(){ command -v "$1" >/dev/null || { echo "Missing: $1" >&2; exit 2; }; }
need gh; need git; mkdir -p "$BASE"

REPO="${1:-}"
[[ -z "$REPO" ]] && { echo "usage: $0 <repo-name> [--public|--private] [--slug <slug>]" >&2; exit 1; }
VIS="--private"
SLUG="seed_$(date -u +%Y%m%d)"
shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --public|--private) VIS="$1"; shift;;
    --slug) SLUG="${2:?}"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 1;;
  esac
done

DST="$BASE/$REPO"
mkdir -p "$DST"; cd "$DST"

copy_if(){ local src="$1"; local dst="$2"; [[ -e "$src" ]] && rsync -a "$src" "$dst" || true; }
if [[ -d "$TEMPLATE" ]]; then
  copy_if "$TEMPLATE/.github" .
  copy_if "$TEMPLATE/.gitattributes" .
  copy_if "$TEMPLATE/.gitignore" .
  copy_if "$TEMPLATE/scripts" .
  copy_if "$TEMPLATE/tools" .
  copy_if "$TEMPLATE/dictionaries" .
  copy_if "$TEMPLATE/10_projects" .
else
  mkdir -p .github/workflows tools dictionaries 10_projects
  cat > .gitignore <<'GI'
.DS_Store
*.bak
*.tmp
__pycache__/
*.pyc
99_archive/
GI
  cat > .gitattributes <<'GA'
* text=auto eol=lf
*.md diff=markdown
*.yaml linguist-language=YAML
GA
  cat > .github/workflows/spellcheck.yml <<'YML'
name: spellcheck
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  spellcheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python -m pip install --upgrade codespell
      - run: codespell
YML
fi

if [[ ! -x tools/integrity.sh ]]; then
  cat > tools/integrity.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT="${1:-}"; CMD="${2:-update}"
[[ -z "$PROJECT" ]] && { echo "usage: $0 <project> [update|verify]"; exit 1; }
P_DIR="$ROOT/10_projects/$PROJECT"; [[ -d "$P_DIR" ]] || { echo "no such project: $PROJECT"; exit 2; }
shopt -s nullglob
files=("$P_DIR"/*.yaml "$P_DIR"/*.yml "$P_DIR"/*.md)
manifest="$P_DIR/manifest.yaml"
update(){ : > "$manifest.tmp"
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
}
verify(){ ok=0
  for f in "${files[@]}"; do
    [[ -f "$f.sha256" ]] || { echo "MISSING: $f.sha256"; ok=1; continue; }
    sha256sum --check --status "$f.sha256" || { echo "FAIL: $f"; ok=1; }
  done
  [[ -f "$manifest.sha256" ]] && sha256sum --check --status "$manifest.sha256" || { echo "FAIL: manifest"; ok=1; }
  if [[ -f "$manifest.asc" ]]; then gpg --verify "$manifest.asc" "$manifest" || ok=1; fi
  exit $ok
}
case "$CMD" in update) update ;; verify) verify ;; *) echo "use: update|verify"; exit 3;; esac
SH
  chmod +x tools/integrity.sh
fi

mkdir -p "10_projects/${SLUG}"
: > "10_projects/${SLUG}/log.md"
echo "title: ${SLUG}" > "10_projects/${SLUG}/meta.yaml"
: > "10_projects/${SLUG}/refs.md"
./tools/integrity.sh "${SLUG}" update

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || git init
git branch -M main
if [[ -f "$BASE/.gitconfig" ]]; then git config --local include.path "../.gitconfig"; fi
if [[ -f "$BASE/.gitignore_global" ]]; then git config --local core.excludesfile "../.gitignore_global"; fi

mkdir -p .git/hooks
if [[ -f scripts/hooks/pre-commit.sample ]]; then
  cp scripts/hooks/pre-commit.sample .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
else
  cat > .git/hooks/pre-commit <<'PC'
#!/usr/bin/env bash
set -e
proj="${PROJECT:-}"; [[ -z "$proj" ]] && proj="$(ls 10_projects | head -n1)"
[ -x tools/integrity.sh ] && ./tools/integrity.sh "$proj" update
PC
  chmod +x .git/hooks/pre-commit
fi

git add .
git commit -m "init: ${REPO} skeleton + ${SLUG} seed + integrity"

if gh repo view "${GH_USER}/${REPO}" >/dev/null 2>&1; then
  git remote set-url origin "git@github.com:${GH_USER}/${REPO}.git" 2>/dev/null || \
  git remote add origin "git@github.com:${GH_USER}/${REPO}.git"
  git push -u origin main
else
  gh repo create "${GH_USER}/${REPO}" ${VIS} --source . --remote origin --push
fi

echo "Done: ${GH_USER}/${REPO} (${VIS#--}) — slug=${SLUG}"
