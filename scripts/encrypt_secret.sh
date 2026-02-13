#!/bin/bash
# encrypt_secret.sh - Encrypt a file using age for git backup

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <input_file> <output_file>"
    echo "Example: $0 openclaw.json config/openclaw.json.age"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"

if [ ! -f "$INPUT" ]; then
    echo "Error: Input file '$INPUT' not found"
    exit 1
fi

# Encrypt with age (symmetric)
/tmp/age/age -o "$OUTPUT" -p "$INPUT"

echo "Encrypted '$INPUT' to '$OUTPUT'"
echo "To decrypt: age -d -i $KEYFILE $OUTPUT"
