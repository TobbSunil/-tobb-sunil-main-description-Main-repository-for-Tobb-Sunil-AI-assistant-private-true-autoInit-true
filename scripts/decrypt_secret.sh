#!/bin/bash
# decrypt_secret.sh - Decrypt a file using age

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <encrypted_file> <output_file> [keyfile]"
    echo "Example: $0 config/openclaw.json.age openclaw.json"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"
KEYFILE="${3:-$HOME/.config/openclaw/age_key.txt}"

if [ ! -f "$INPUT" ]; then
    echo "Error: Encrypted file '$INPUT' not found"
    exit 1
fi

# Decrypt with age
if [ -f "$KEYFILE" ]; then
    /tmp/age/age -d -i "$KEYFILE" "$INPUT" > "$OUTPUT"
else
    /tmp/age/age -d "$INPUT" > "$OUTPUT"
fi

chmod 600 "$OUTPUT"
echo "Decrypted '$INPUT' to '$OUTPUT'"
