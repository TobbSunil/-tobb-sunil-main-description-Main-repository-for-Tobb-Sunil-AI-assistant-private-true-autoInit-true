#!/bin/bash
# encrypt_all_secrets.sh - Encrypt all OpenClaw secrets

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$SCRIPT_DIR/.."
OPENCLAW_DIR="$HOME/.openclaw"

echo "Encrypting OpenClaw secrets..."

# Create age key if needed
if [ ! -f "$HOME/.config/openclaw/age_key.txt" ]; then
    echo "Generating age key..."
    mkdir -p "$HOME/.config/openclaw"
    /tmp/age/age-keygen -o "$HOME/.config/openclaw/age_key.txt" 2>/dev/null
    cat "$HOME/.config/openclaw/age_key.txt" | grep "# public key:" > "$HOME/.config/openclaw/age_key.pub"
    chmod 600 "$HOME/.config/openclaw/age_key.txt"
    echo "Key generated."
fi

# Get public key
PUB_KEY=$(cat "$HOME/.config/openclaw/age_key.pub" | grep -o "age1[a-zA-Z0-9]*")

echo "Using public key: $PUB_KEY"

# Encrypt sensitive files
echo "Encrypting openclaw.json..."
/tmp/age/age -o "$REPO_DIR/config/openclaw.json.age" -r "$PUB_KEY" "$OPENCLAW_DIR/openclaw.json"

echo "Encrypting mcporter.json..."
/tmp/age/age -o "$REPO_DIR/config/mcporter.json.age" -r "$PUB_KEY" "$HOME/.openclaw/workspace/config/mcporter.json"

# Create README for encrypted configs
cat > "$REPO_DIR/config/README.md" << 'EOF'
# Encrypted Configs

This directory contains encrypted versions of sensitive OpenClaw configuration files.

## Files

- `openclaw.json.age` - Encrypted main OpenClaw config
- `mcporter.json.age` - Encrypted MCP server config

## Decrypting

```bash
age -d -i ~/.config/openclaw/age_key.txt openclaw.json.age > openclaw.json
age -d -i ~/.config/openclaw/age_key.txt mcporter.json.age > mcporter.json
```

## Security Notes

- Never commit unencrypted config files to git
- Keep your age key file secure (`~/.config/openclaw/age_key.txt`)
- The public key (`age_key.pub`) can be shared with trusted machines
EOF

echo ""
echo "✅ Encryption complete!"
echo ""
echo "Encrypted files:"
echo "  - config/openclaw.json.age"
echo "  - config/mcporter.json.age"
echo ""
echo "Add them to git:"
echo "  git add config/*.age config/README.md"
echo ""
echo "To decrypt on another machine:"
echo "  age -d -i ~/.config/openclaw/age_key.txt config/openclaw.json.age > openclaw.json"
echo ""
