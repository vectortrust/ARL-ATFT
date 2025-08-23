#!/usr/bin/env bash
# Bootstrap: atlas-memory-trust + arl-atft (spellcheck integrated)
# Mode: high security, low drag
set -euo pipefail

echo "=== Bootstrap: Memory Trust + ATFT (with spellcheck) ==="

# --- Inputs ---
read -r -p "Path to atlas-memory-trust.zip [./atlas-memory-trust.zip]: " MT_ZIP
MT_ZIP=${MT_ZIP:-./atlas-memory-trust.zip}
read -r -p "Path to arl-atft_skeleton.zip [./arl-atft_skeleton.zip]: " ATFT_ZIP
ATFT_ZIP=${ATFT_ZIP:-./arl-atft_skeleton.zip}

read -r -p "Memory Trust repo URL (SSH): " MT_URL
read -r -p "ATFT repo URL (SSH): " ATFT_URL
read -r -p "Initial Memory Trust project slug (e.g., amon_turing_2025): " PROJ

# --- Checks ---
for f in "$MT_ZIP" "$ATFT_ZIP"; do [[ -f "$f" ]] || { echo "Missing: $f"; exit 2; }; done
	command -v git >/dev/null || { echo "git not found"; exit 3; }
	command -v unzip >/dev/null || { echo "unzip not found"; exit 4; }
	command -v sha256sum >/dev/null || { echo "sha256sum not found"; exit 5; }
	# gpg optional
	
	# --- Helpers ---
	signed_commit() {
		local msg="$1"
		if git config --get commit.gpgsign >/dev/null; then
			git commit -S -m "$msg" || git commit -m "$msg"
			else
				if gpg --list-secret-keys >/dev/null 2>&1; then git config commit.gpgsign true || true; fi
					git commit -S -m "$msg" || git commit -m "$msg"
					fi
	}
	
	add_spellcheck() {
		# $1 = repo root
		local ROOT="$1"
		mkdir -p "$ROOT/dictionaries" "$ROOT/tools" "$ROOT/.github/workflows"
		
		# .codespellrc
		cat > "$ROOT/.codespellrc" <<'RC'
		
		[codespell]
		skip = ./.git,./99_archive,*.png,*.jpg,*.pdf,*.svg,*.tgz,*.zip,*.tar,*.gz
		ignore-words = dictionaries/allowlist.txt
		check-hidden = false
		count = true
		quiet-level = 3
		RC
		
		# allowlist
		cat > "$ROOT/dictionaries/allowlist.txt" <<'WL'
		# domain-specific tokens to ignore (one per line)
		teh
		artefact
		behaviour
		colour
		# project terms
		ATFT
		BMF
		Morphogenic
		WL
		
		# local runner
		cat > "$ROOT/tools/spellcheck.sh" <<'SC'
		#!/usr/bin/env bash
		set -euo pipefail
		if ! command -v codespell >/dev/null 2>&1; then
		python3 -m pip install --user --upgrade codespell >/dev/null
		fi
		codespell "${@:-.}"
		SC
		chmod +x "$ROOT/tools/spellcheck.sh"
		
		# CI workflow
		cat > "$ROOT/.github/workflows/spellcheck.yml" <<'YML'
		name: spellcheck
		on:
		push: { branches: [ main ] }
		pull_request: { branches: [ main ] }
		jobs:
		spellcheck:
		runs-on: ubuntu-latest
		steps:
		- uses: actions/checkout@v4
		- uses: actions/setup-python@v5
		with: { python-version: '3.11' }
		- name: Install codespell
		run: python -m pip install --upgrade codespell
		- name: Run codespell
		run: codespell
		YML}
	
	# --- 1) Memory Trust ---
	echo "[1/2] Setting up atlas-memory-trust…"
	rm -rf atlas-memory-trust
	unzip -q "$MT_ZIP" -d .
	cd atlas-memory-trust
	
	git init -b main
	git add .
	signed_commit "init: atlas-memory-trust skeleton"
	
	# pre-commit hook
	if [[ -f scripts/hooks/pre-commit.sample ]]; then
		mkdir -p .git/hooks
		cp scripts/hooks/pre-commit.sample .git/hooks/pre-commit
		chmod +x .git/hooks/pre-commit
		fi
		
		# first project + integrity
		if [[ -d 10_projects/example ]]; then
			cp -r 10_projects/example "10_projects/${PROJ}"
			fi
			if [[ -x tools/integrity.sh ]]; then
				./tools/integrity.sh "${PROJ}" update
				git add "10_projects/${PROJ}/manifest.yaml" "10_projects/${PROJ}/"*.sha256 || true
				signed_commit "proj: start ${PROJ} + checksums"
				fi
				
				# spellcheck integration
				add_spellcheck "$(pwd)"
				git add .codespellrc dictionaries tools/spellcheck.sh .github/workflows/spellcheck.yml
				signed_commit "chore: add spellcheck (codespell + CI)"
				
				git remote add origin "$MT_URL"
				git push -u origin main
				cd ..
				
				# --- 2) ARL-ATFT ---
				echo "[2/2] Setting up ARL-ATFT…"
				rm -rf arl-atft
				unzip -q "$ATFT_ZIP" -d .
				cd arl-atft
				
				git init -b main
				git add .
				signed_commit "init: ARL-ATFT skeleton"
				
				# spellcheck integration
				add_spellcheck "$(pwd)"
				git add .codespellrc dictionaries tools/spellcheck.sh .github/workflows/spellcheck.yml
				signed_commit "chore: add spellcheck (codespell + CI)"
				
				git remote add origin "$ATFT_URL"
				git push -u origin main
				
				echo "=== Done. Repos pushed ==="
				echo "Next:"
				echo " - Enable branch protection on 'main' in both repos."
				echo " - Verify Actions: 'spellcheck' (both) and 'verify-integrity' (atlas-memory-trust)."
				echo " - Drop latest ATFT PDF into papers/ and commit."
				
