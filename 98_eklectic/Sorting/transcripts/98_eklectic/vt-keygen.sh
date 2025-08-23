#!/bin/bash
# Vector Trust: Secure GPG Key Creation (Ed25519 + Git integration)

set -e

NAME="Vector Trust"
EMAIL="vectortrust@protonmail.com"
KEYFILE_DIR="/home/nfs/vtrust/vt-cis/vt_keys"
KEYFILE_PUB="$KEYFILE_DIR/vt_public.asc"
KEYFILE_SEC="$KEYFILE_DIR/vt_private.sec.asc"

mkdir -p "$KEYFILE_DIR"

echo "[+] Generating Ed25519 GPG key for $NAME <$EMAIL>..."
gpg --batch --passphrase '' --quick-gen-key "$NAME <$EMAIL>" ed25519 sign 1y

KEYID=$(gpg --list-secret-keys --keyid-format LONG "$EMAIL" | grep 'sec' | awk '{print $2}' | cut -d'/' -f2)

echo "[+] Key ID: $KEYID"

echo "[+] Exporting public key to $KEYFILE_PUB"
gpg --armor --output "$KEYFILE_PUB" --export "$EMAIL"

echo "[+] Exporting PRIVATE key to $KEYFILE_SEC (LOCK THIS DOWN!)"
gpg --armor --output "$KEYFILE_SEC" --export-secret-keys "$EMAIL"

echo "[+] Configuring Git to use this key..."
git config --global user.name "$NAME"
git config --global user.email "$EMAIL"
git config --global user.signingkey "$KEYID"
git config --global commit.gpgsign true

echo "[✓] All set. Your Vector Trust"

